import json
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Annotated, Optional

import requests
import typer
from dotenv import load_dotenv

from utils import CONTEXT_SETTINGS

cvat_app = typer.Typer(help="CVAT operations.", context_settings=CONTEXT_SETTINGS)
project_app = typer.Typer(help="Project operations.", context_settings=CONTEXT_SETTINGS)
task_app = typer.Typer(help="Task operations.", context_settings=CONTEXT_SETTINGS)
cvat_app.add_typer(project_app, name="project")
cvat_app.add_typer(task_app, name="task")


class TableFormatter:
    """Utility class for formatting data as human-readable tables."""

    @staticmethod
    def format_projects_table(projects_data: dict) -> str:
        """Format projects list as a readable table."""
        if not projects_data or "results" not in projects_data:
            return "No projects found"

        projects = projects_data["results"]
        if not projects:
            return "No projects found"

        # Create header
        header = ["ID", "Name", "Owner", "Status", "Tasks", "Created"]
        separator = "-" * 80

        # Format each project
        lines = [separator]
        lines.append(
            f"{header[0]:<4} {header[1]:<20} {header[2]:<12} {header[3]:<12} {header[4]:<6} {header[5]:<16}"
        )
        lines.append(separator)

        for project in projects:
            project_id = str(project.get("id", ""))
            name = project.get("name", "")[:18] + (
                ".." if len(project.get("name", "")) > 18 else ""
            )
            owner = project.get("owner", {}).get("username", "")[:10] + (
                ".." if len(project.get("owner", {}).get("username", "")) > 10 else ""
            )
            status = project.get("status", "")[:10]
            tasks_count = str(project.get("tasks", {}).get("count", 0))
            created = project.get("created_date", "")[:10]  # Just date part

            lines.append(
                f"{project_id:<4} {name:<20} {owner:<12} {status:<12} {tasks_count:<6} {created:<16}"
            )

        lines.append(separator)
        lines.append(f"Total: {len(projects)} project(s)")

        return "\n".join(lines)

    # @staticmethod
    # def format_tasks_table(tasks_data: dict) -> str:
    #     """Format tasks list as a readable table."""
    #     if not tasks_data or "results" not in tasks_data:
    #         return "No tasks found"

    #     tasks = tasks_data["results"]
    #     if not tasks:
    #         return "No tasks found"

    #     # Create header
    #     header = ["ID", "Name", "Project ID", "Owner", "Status", "Size", "Created"]
    #     separator = "-" * 90

    #     # Format each task
    #     lines = [separator]
    #     lines.append(
    #         f"{header[0]:<4} {header[1]:<20} {header[2]:<10} {header[3]:<12} {header[4]:<12} {header[5]:<6} {header[6]:<16}"
    #     )
    #     lines.append(separator)

    #     for task in tasks:
    #         task_id = str(task.get("id", ""))
    #         name = task.get("name", "")[:18] + (
    #             ".." if len(task.get("name", "")) > 18 else ""
    #         )
    #         project_id = str(task.get("project_id", "-"))
    #         owner = task.get("owner", {}).get("username", "")[:10] + (
    #             ".." if len(task.get("owner", {}).get("username", "")) > 10 else ""
    #         )
    #         status = task.get("status", "")[:10]
    #         size = str(task.get("size", 0))
    #         created = task.get("created_date", "")[:10]  # Just date part

    #         lines.append(
    #             f"{task_id:<4} {name:<20} {project_id:<10} {owner:<12} {status:<12} {size:<6} {created:<16}"
    #         )

    #     lines.append(separator)

    #     # Add summary information
    #     total_tasks = len(tasks)
    #     completed_tasks = sum(1 for t in tasks if t.get("status") == "completed")
    #     in_progress_tasks = sum(1 for t in tasks if t.get("status") == "annotation")

    #     lines.append(
    #         f"Total: {total_tasks} task(s) | Completed: {completed_tasks} | In Progress: {in_progress_tasks}"
    #     )

    #     return "\n".join(lines)


class CVATApi:
    """A class to interact with the CVAT REST API without the CVAT-SDK."""

    def __init__(self, url, username, password):
        if not url:
            raise ValueError("CVAT_URL cannot be empty.")
        self.base_url = url.rstrip("/")
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self._login(username, password)

    def _login(self, username, password):
        """Authenticate and store session token."""
        login_url = f"{self.api_url}/auth/login"
        try:
            response = self.session.post(
                login_url, json={"username": username, "password": password}
            )
            response.raise_for_status()
            token = response.json()["key"]
            self.session.headers.update({"Authorization": f"Token {token}"})
            print("Successfully logged in to CVAT.", file=sys.stderr)
        except requests.exceptions.RequestException as e:
            print(f"Login failed: {e}", file=sys.stderr)
            if e.response is not None:
                print(f"Response: {e.response.text}", file=sys.stderr)
            sys.exit(1)

    def _handle_error(self, response, message):
        """Generic error handler for API responses."""
        if response.status_code >= 400:
            error_message = (
                f"Error: {message}\n"
                f"Status Code: {response.status_code}\n"
                f"Response: {response.text}"
            )
            raise requests.exceptions.HTTPError(error_message, response=response)

    def wait_for_job(self, rq_id):
        """Poll the status of an asynchronous job."""
        request_url = f"{self.api_url}/requests/{rq_id}"
        print(f"Waiting for job {rq_id} to complete...", file=sys.stderr)
        while True:
            response = self.session.get(request_url)
            self._handle_error(response, f"Failed to get job status for {rq_id}")
            data = response.json()
            status = data.get("status")
            print(f"Job {rq_id} status: {status}", file=sys.stderr)

            if status == "finished":
                return data
            if status == "failed":
                raise Exception(
                    f"Job {rq_id} failed: {data.get('message', 'No message')}"
                )
            if status not in ["queued", "started"]:
                raise Exception(f"Unknown job status for {rq_id}: {status}")

            time.sleep(2)

    def _download_file(self, url, output_path):
        """Download a file with streaming."""
        print(f"Downloading from {url} to {output_path}...", file=sys.stderr)
        with self.session.get(url, stream=True) as r:
            self._handle_error(r, "File download failed")
            with open(output_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        print("Download complete.", file=sys.stderr)

    def get_task_metadata(self, task_id):
        """Retrieve task metadata (labels, attributes)."""
        url = f"{self.api_url}/tasks/{task_id}"
        response = self.session.get(url)
        self._handle_error(response, f"Failed to get metadata for task {task_id}")
        return response.json()

    def get_task_labels(self, task_id):
        """Retrieve all labels for a specific task."""
        # Use a large page size to avoid pagination for labels
        url = f"{self.api_url}/labels?task_id={task_id}&page_size=1000"
        response = self.session.get(url)
        self._handle_error(response, f"Failed to get labels for task {task_id}")
        # The response is paginated, we want the results
        return response.json().get("results", [])

    def get_task_data_meta(self, task_id):
        """Retrieve task data metadata (frame mapping)."""
        url = f"{self.api_url}/tasks/{task_id}/data/meta"
        response = self.session.get(url)
        self._handle_error(response, f"Failed to get data meta for task {task_id}")
        return response.json()

    def patch_annotations(self, task_id, payload):
        """Upload annotations via PATCH to append new shapes."""
        url = f"{self.api_url}/tasks/{task_id}/annotations?action=create"
        # Using json parameter automatically sets Content-Type: application/json
        response = self.session.patch(url, json=payload)
        self._handle_error(response, f"Failed to patch annotations for task {task_id}")
        return response.json()

    # --- Project Operations ---

    def create_project(self, name):
        """Create a new project."""
        url = f"{self.api_url}/projects"
        response = self.session.post(url, json={"name": name})
        self._handle_error(response, f"Failed to create project '{name}'")
        project_data = response.json()
        print(
            f"Successfully created project '{name}' with ID: {project_data['id']}",
            file=sys.stderr,
        )
        return project_data

    def list_projects(self):
        """List all projects."""
        url = f"{self.api_url}/projects?page_size=100"  # Get more items per page
        response = self.session.get(url)
        self._handle_error(response, "Failed to list projects")
        return response.json()

    def delete_project(self, project_id):
        """Delete a project."""
        url = f"{self.api_url}/projects/{project_id}"
        response = self.session.delete(url)
        if response.status_code != 204:
            self._handle_error(response, f"Failed to delete project {project_id}")
        print(f"Project {project_id} deleted successfully.", file=sys.stderr)

    def backup_project(self, project_id, output_file):
        """Backup a project."""
        url = f"{self.api_url}/projects/{project_id}/backup/export"
        response = self.session.post(url)
        self._handle_error(
            response, f"Failed to trigger backup for project {project_id}"
        )

        if response.status_code != 202:
            raise Exception(
                f"Unexpected status code for backup trigger: {response.status_code}\n{response.text}"
            )

        rq_id = response.json().get("rq_id")
        if not rq_id:
            raise Exception("Could not get request ID for backup job.")

        job_result = self.wait_for_job(rq_id)
        download_url = job_result.get("result_url")
        if not download_url:
            raise Exception("Job finished but no result_url found.")

        if not download_url.startswith(("http://", "https://")):
            download_url = f"{self.base_url}{download_url}"

        self._download_file(download_url, output_file)

    def import_project(self, backup_file):
        """Import a project from a backup."""
        url = f"{self.api_url}/projects/backup"
        with open(backup_file, "rb") as f:
            files = {"project_file": (Path(backup_file).name, f, "application/zip")}
            response = self.session.post(url, files=files)
        self._handle_error(response, f"Failed to import project from {backup_file}")

        if response.status_code == 202:
            rq_id = response.json().get("rq_id")
            self.wait_for_job(rq_id)
            print("Project import job finished.", file=sys.stderr)
        else:
            print("Project import started.", file=sys.stderr)

    def export_project_dataset(
        self, project_id, output_file, format_name, save_images=True, only_manual=False
    ):
        """Export a project's dataset."""
        url = f"{self.api_url}/projects/{project_id}/dataset/export"
        params = {"format": format_name, "save_images": save_images}

        if only_manual:
            # CVAT uses a JSON-based logic for filtering.
            # This filter ensures only annotations with source 'manual' are included.
            filter_logic = {"and": [{"==": [{"var": "source"}, "manual"]}]}
            params["filter"] = json.dumps(filter_logic)

        response = self.session.post(url, params=params)
        self._handle_error(
            response, f"Failed to trigger export for project {project_id}"
        )

        if response.status_code != 202:
            raise Exception(
                f"Unexpected status code for export trigger: {response.status_code}\n{response.text}"
            )

        rq_id = response.json().get("rq_id")
        if not rq_id:
            raise Exception("Could not get request ID for export job.")

        job_result = self.wait_for_job(rq_id)
        download_url = job_result.get("result_url")
        if not download_url:
            raise Exception("Job finished but no result_url found.")

        if not download_url.startswith(("http://", "https://")):
            download_url = f"{self.base_url}{download_url}"

        self._download_file(download_url, output_file)

    def import_project_dataset(self, project_id, dataset_file, format_name):
        """Import a dataset into a project."""
        url = f"{self.api_url}/projects/{project_id}/dataset"
        params = {"format": format_name}
        with open(dataset_file, "rb") as f:
            files = {"dataset_file": (Path(dataset_file).name, f)}
            response = self.session.post(url, params=params, files=files)
        self._handle_error(
            response, f"Failed to import dataset for project {project_id}"
        )

        if response.status_code == 202:
            rq_id = response.json().get("rq_id")
            self.wait_for_job(rq_id)
            print("Dataset import job finished.", file=sys.stderr)
        else:
            print("Dataset import started.", file=sys.stderr)

    # # --- Task Operations ---

    # def create_task(self, name, project_id):
    #     """Create a new task."""
    #     url = f"{self.api_url}/tasks"
    #     payload = {"name": name}
    #     if project_id:
    #         payload["project_id"] = project_id

    #     response = self.session.post(url, json=payload)
    #     self._handle_error(response, f"Failed to create task '{name}'")
    #     task_data = response.json()
    #     print(f"Successfully created task '{name}' with ID: {task_data['id']}")
    #     return task_data

    # def attach_data_to_task(self, task_id, image_paths):
    #     """Attach data (images) to a task."""
    #     data_url = f"{self.api_url}/tasks/{task_id}/data"
    #     files_to_upload = []
    #     try:
    #         for p in image_paths:
    #             files_to_upload.append(("client_files", open(p, "rb")))

    #         data = {"image_quality": 70}
    #         response = self.session.post(data_url, data=data, files=files_to_upload)
    #         self._handle_error(response, f"Failed to upload images to task {task_id}")

    #         if response.status_code == 202:
    #             rq_id = response.json().get("rq_id")
    #             self.wait_for_job(rq_id)
    #             print("Image upload job finished.")
    #         else:
    #             print(
    #                 f"Successfully uploaded {len(image_paths)} images to task {task_id}."
    #             )
    #     finally:
    #         for _, f in files_to_upload:
    #             f.close()

    # def list_tasks(self):
    #     """List all tasks."""
    #     url = f"{self.api_url}/tasks?page_size=100"  # Get more items per page
    #     response = self.session.get(url)
    #     self._handle_error(response, "Failed to list tasks")
    #     return response.json()

    # def delete_task(self, task_id):
    #     """Delete a task."""
    #     url = f"{self.api_url}/tasks/{task_id}"
    #     response = self.session.delete(url)
    #     if response.status_code != 204:
    #         self._handle_error(response, f"Failed to delete task {task_id}")
    #     print(f"Task {task_id} deleted successfully.")

    # def backup_task(self, task_id, output_file):
    #     """Backup a task."""
    #     url = f"{self.api_url}/tasks/{task_id}/backup/export"
    #     response = self.session.post(url)
    #     self._handle_error(response, f"Failed to trigger backup for task {task_id}")

    #     if response.status_code != 202:
    #         raise Exception(
    #             f"Unexpected status code for backup trigger: {response.status_code}\n{response.text}"
    #         )

    #     rq_id = response.json().get("rq_id")
    #     if not rq_id:
    #         raise Exception("Could not get request ID for backup job.")

    #     job_result = self.wait_for_job(rq_id)
    #     download_url = job_result.get("result_url")
    #     if not download_url:
    #         raise Exception("Job finished but no result_url found.")

    #     if not download_url.startswith(("http://", "https://")):
    #         download_url = f"{self.base_url}{download_url}"

    #     self._download_file(download_url, output_file)

    # def import_task(self, backup_file):
    #     """Import a task from a backup."""
    #     url = f"{self.api_url}/tasks/backup"
    #     with open(backup_file, "rb") as f:
    #         files = {"task_file": (Path(backup_file).name, f, "application/zip")}
    #         response = self.session.post(url, files=files)
    #     self._handle_error(response, f"Failed to import task from {backup_file}")

    #     if response.status_code == 202:
    #         rq_id = response.json().get("rq_id")
    #         self.wait_for_job(rq_id)
    #         print("Task import job finished.")
    #     else:
    #         print("Task import started.")

    def export_task_dataset(
        self, task_id, output_file, format_name, save_images=True, only_manual=False
    ):
        """Export a task's dataset."""
        url = f"{self.api_url}/tasks/{task_id}/dataset/export"
        params = {"format": format_name, "save_images": save_images}

        if only_manual:
            filter_logic = {"and": [{"==": [{"var": "source"}, "manual"]}]}
            params["filter"] = json.dumps(filter_logic)

        response = self.session.post(url, params=params)
        self._handle_error(
            response, f"Failed to trigger dataset export for task {task_id}"
        )

        if response.status_code != 202:
            raise Exception(
                f"Unexpected status code for export trigger: {response.status_code}\n{response.text}"
            )

        rq_id = response.json().get("rq_id")
        if not rq_id:
            raise Exception("Could not get request ID for export job.")

        job_result = self.wait_for_job(rq_id)
        download_url = job_result.get("result_url")
        if not download_url:
            raise Exception("Job finished but no result_url found.")

        if not download_url.startswith(("http://", "https://")):
            download_url = f"{self.base_url}{download_url}"

        self._download_file(download_url, output_file)

    # def import_annotations(self, task_id, annotations_file, format_name):
    #     """Import annotations into a task."""
    #     url = f"{self.api_url}/tasks/{task_id}/annotations/"
    #     params = {"format": format_name}

    #     with open(annotations_file, "rb") as f:
    #         files = {"annotation_file": (Path(annotations_file).name, f)}
    #         response = self.session.post(url, params=params, files=files)

    #     self._handle_error(response, f"Failed to import annotations for task {task_id}")

    #     if response.status_code == 202:  # Asynchronous
    #         rq_id = response.json().get("rq_id")
    #         if not rq_id:
    #             raise Exception("Could not get request ID for annotation upload job.")
    #         self.wait_for_job(rq_id)
    #         print("Annotation upload job finished.")
    #     elif response.status_code == 201:  # Synchronous
    #         print("Annotations imported successfully.")


def _get_api():
    load_dotenv()
    return CVATApi(
        os.getenv("CVAT_URL"),
        os.getenv("CVAT_USERNAME"),
        os.getenv("CVAT_PASSWORD"),
    )


@project_app.command("create")
def project_create(name: str):
    _get_api().create_project(name)


@project_app.command("list")
def project_list():
    api = _get_api()
    print(TableFormatter.format_projects_table(api.list_projects()))


@project_app.command("delete")
def project_delete(project_id: int):
    _get_api().delete_project(project_id)


@project_app.command("backup")
def project_backup(project_id: int, output_file: Path):
    _get_api().backup_project(project_id, str(output_file))
    print(output_file)


@project_app.command("recreate")
def project_recreate(input_file: Path):
    _get_api().import_project(str(input_file))


@project_app.command("import_dataset")
def project_import_dataset(
    project_id: Annotated[int, typer.Option("--project-id", "-u")],
    input_file: Annotated[Path, typer.Option("--input-file", "-i")],
    format_name: Annotated[str, typer.Option("--format", "-f", help="yolo or cvat")],
):
    if not input_file.is_file() or input_file.suffix.lower() != ".zip":
        print(
            f"Error: Input file must be a .zip file. Got: {input_file}", file=sys.stderr
        )
        sys.exit(1)

    format_map = {"yolo": "YOLO 1.1", "cvat": "CVAT 1.1"}
    cvat_format = format_map.get(format_name.lower())
    if not cvat_format:
        print(f"Error: Unsupported format {format_name}", file=sys.stderr)
        sys.exit(1)

    _get_api().import_project_dataset(project_id, str(input_file), cvat_format)


@project_app.command("export_dataset")
def project_export_dataset(
    project_id: Annotated[int, typer.Option("--project-id", "-u")],
    output_file: Annotated[Path, typer.Option("--output-file", "-o")],
    format_name: Annotated[str, typer.Option("--format", "-f")] = "YOLO 1.1",
    images: Annotated[bool, typer.Option("--images/--no-images")] = True,
    only_manual: bool = False,
):
    _get_api().export_project_dataset(
        project_id, str(output_file), format_name, images, only_manual
    )
    print(output_file)


@task_app.command("export_dataset")
def task_export_dataset(
    task_id: Annotated[int, typer.Option("--task-id", "-tid")],
    output_file: Annotated[Path, typer.Option("--output-file", "-o")],
    format_name: Annotated[str, typer.Option("--format", "-f")] = "YOLO 1.1",
    images: Annotated[bool, typer.Option("--images/--no-images")] = True,
    only_manual: bool = False,
):
    _get_api().export_task_dataset(
        task_id, str(output_file), format_name, images, only_manual
    )
    print(output_file)
