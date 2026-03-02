import json
import os
import shutil
import sys
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

        header = ["ID", "Name", "Owner", "Status", "Tasks", "Created"]
        separator = "-" * 80

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
            created = project.get("created_date", "")[:10]

            lines.append(
                f"{project_id:<4} {name:<20} {owner:<12} {status:<12} {tasks_count:<6} {created:<16}"
            )

        lines.append(separator)
        lines.append(f"Total: {len(projects)} project(s)")

        return "\n".join(lines)


class CVATApi:
    """A class to interact with the CVAT REST API without the CVAT-SDK."""

    def __init__(
        self, url: Optional[str], username: Optional[str], password: Optional[str]
    ):
        if not url:
            raise ValueError("CVAT_URL cannot be empty.")
        self.base_url = url.rstrip("/")
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self._login(username, password)

    def _login(self, username: Optional[str], password: Optional[str]) -> None:
        """Authenticate and store session token."""
        if not username or not password:
            raise ValueError("CVAT credentials missing.")

        login_url = f"{self.api_url}/auth/login"
        try:
            response = self.session.post(
                login_url, json={"username": username, "password": password}
            )
            response.raise_for_status()
            token = response.json()["key"]
            self.session.headers.update({"Authorization": f"Token {token}"})
            print("Successfully logged in to CVAT.")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Login failed: {e}")

    def _handle_error(self, response: requests.Response, message: str) -> None:
        """Generic error handler for API responses."""
        if response.status_code < 400:
            return

        error_message = (
            f"Error: {message}\n"
            f"Status Code: {response.status_code}\n"
            f"Response: {response.text}"
        )
        raise requests.exceptions.HTTPError(error_message, response=response)

    def wait_for_job(self, rq_id: str) -> dict:
        """Poll the status of an asynchronous job."""
        import time

        request_url = f"{self.api_url}/requests/{rq_id}"
        print(f"Waiting for job {rq_id} to complete...")
        while True:
            response = self.session.get(request_url)
            self._handle_error(response, f"Failed to get job status for {rq_id}")

            data = response.json()
            status = data.get("status")
            print(f"Job {rq_id} status: {status}")

            if status == "finished":
                return data
            if status == "failed":
                raise Exception(
                    f"Job {rq_id} failed: {data.get('message', 'No message')}"
                )
            if status not in ["queued", "started"]:
                raise Exception(f"Unknown job status for {rq_id}: {status}")

            time.sleep(2)

    def _download_file(self, url: str, output_path: str) -> None:
        """Download a file with streaming."""
        print(f"Downloading from {url} to {output_path}...")
        with self.session.get(url, stream=True) as r:
            self._handle_error(r, "File download failed")
            with open(output_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        print("Download complete.")

    def get_task_metadata(self, task_id: int) -> dict:
        """Retrieve task metadata (labels, attributes)."""
        url = f"{self.api_url}/tasks/{task_id}"
        response = self.session.get(url)
        self._handle_error(response, f"Failed to get metadata for task {task_id}")
        return response.json()

    def get_task_labels(self, task_id: int) -> list:
        """Retrieve all labels for a specific task."""
        url = f"{self.api_url}/labels?task_id={task_id}&page_size=1000"
        response = self.session.get(url)
        self._handle_error(response, f"Failed to get labels for task {task_id}")
        return response.json().get("results", [])

    def get_task_data_meta(self, task_id: int) -> dict:
        """Retrieve task data metadata (frame mapping)."""
        url = f"{self.api_url}/tasks/{task_id}/data/meta"
        response = self.session.get(url)
        self._handle_error(response, f"Failed to get data meta for task {task_id}")
        return response.json()

    def patch_annotations(self, task_id: int, payload: dict) -> dict:
        """Upload annotations via PATCH to append new shapes."""
        url = f"{self.api_url}/tasks/{task_id}/annotations?action=create"
        response = self.session.patch(url, json=payload)
        self._handle_error(response, f"Failed to patch annotations for task {task_id}")
        return response.json()

    def create_project(self, name: str) -> dict:
        """Create a new project."""
        url = f"{self.api_url}/projects"
        response = self.session.post(url, json={"name": name})
        self._handle_error(response, f"Failed to create project '{name}'")
        project_data = response.json()
        print(f"Successfully created project '{name}' with ID: {project_data['id']}")
        return project_data

    def list_projects(self) -> dict:
        """List all projects."""
        url = f"{self.api_url}/projects?page_size=100"
        response = self.session.get(url)
        self._handle_error(response, "Failed to list projects")
        return response.json()

    def delete_project(self, project_id: int) -> None:
        """Delete a project."""
        url = f"{self.api_url}/projects/{project_id}"
        response = self.session.delete(url)
        if response.status_code != 204:
            self._handle_error(response, f"Failed to delete project {project_id}")
        print(f"Project {project_id} deleted successfully.")

    def backup_project(self, project_id: int, output_file: str) -> None:
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

    def import_project(self, backup_file: str) -> None:
        """Import a project from a backup."""
        url = f"{self.api_url}/projects/backup"
        with open(backup_file, "rb") as f:
            files = {"project_file": (Path(backup_file).name, f, "application/zip")}
            response = self.session.post(url, files=files)
        self._handle_error(response, f"Failed to import project from {backup_file}")

        if response.status_code == 202:
            rq_id = response.json().get("rq_id")
            self.wait_for_job(rq_id)
            print("Project import job finished.")
        else:
            print("Project import started.")

    def export_project_dataset(
        self,
        project_id: int,
        output_file: str,
        format_name: str,
        save_images: bool = True,
        only_manual: bool = False,
    ) -> None:
        """Export a project's dataset."""
        url = f"{self.api_url}/projects/{project_id}/dataset/export"
        params = {"format": format_name, "save_images": save_images}

        if only_manual:
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

    def import_project_dataset(
        self, project_id: int, dataset_file: str, format_name: str
    ) -> None:
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
            print("Dataset import job finished.")
        else:
            print("Dataset import started.")

    def export_task_dataset(
        self,
        task_id: int,
        output_file: str,
        format_name: str,
        save_images: bool = True,
        only_manual: bool = False,
    ) -> None:
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


def _get_api() -> CVATApi:
    load_dotenv()
    return CVATApi(
        os.getenv("CVAT_URL"),
        os.getenv("CVAT_USERNAME"),
        os.getenv("CVAT_PASSWORD"),
    )


@project_app.command("create")
def project_create(name: str) -> None:
    _get_api().create_project(name)


@project_app.command("list")
def project_list() -> None:
    api = _get_api()
    print(TableFormatter.format_projects_table(api.list_projects()))


@project_app.command("delete")
def project_delete(project_id: int) -> None:
    _get_api().delete_project(project_id)


@project_app.command("backup")
def project_backup(project_id: int, output_file: Path) -> None:
    _get_api().backup_project(project_id, str(output_file))
    print(output_file)


@project_app.command("import")
def project_import(input_file: Path) -> None:
    _get_api().import_project(str(input_file))


@project_app.command("import_dataset")
def project_import_dataset(
    project_id: Annotated[int, typer.Option("--project-id", "-u")],
    input_file: Annotated[Path, typer.Option("--input-file", "-i")],
    format_name: Annotated[str, typer.Option("--format", "-f", help="yolo or cvat")],
) -> None:
    if not input_file.is_file() or input_file.suffix.lower() != ".zip":
        raise ValueError(f"Input file must be a .zip file. Got: {input_file}")

    format_map = {"yolo": "YOLO 1.1", "cvat": "CVAT 1.1"}
    cvat_format = format_map.get(format_name.lower())
    if not cvat_format:
        raise ValueError(f"Unsupported format {format_name}")

    _get_api().import_project_dataset(project_id, str(input_file), cvat_format)


@project_app.command("export_dataset")
def project_export_dataset(
    project_id: Annotated[int, typer.Option("--project-id", "-u")],
    output_file: Annotated[Path, typer.Option("--output-file", "-o")],
    format_name: Annotated[str, typer.Option("--format", "-f")] = "YOLO 1.1",
    images: Annotated[bool, typer.Option("--images/--no-images")] = True,
    only_manual: bool = False,
) -> None:
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
) -> None:
    _get_api().export_task_dataset(
        task_id, str(output_file), format_name, images, only_manual
    )
    print(output_file)
