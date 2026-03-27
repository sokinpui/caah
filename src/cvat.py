import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Annotated, Optional

import requests
import typer
from dotenv import load_dotenv
from converter import concat_datasets

from utils import CONTEXT_SETTINGS, extract_zip

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

    @staticmethod
    def format_tasks_table(tasks_data: dict) -> str:
        """Format tasks list as a readable table."""
        if not tasks_data or "results" not in tasks_data:
            return "No tasks found"

        tasks = tasks_data["results"]
        if not tasks:
            return "No tasks found"

        header = ["ID", "Name", "Status", "Assignee", "Created"]
        separator = "-" * 80

        lines = [separator]
        lines.append(
            f"{header[0]:<6} {header[1]:<30} {header[2]:<12} {header[3]:<15} {header[4]:<12}"
        )
        lines.append(separator)

        for task in tasks:
            tid = str(task.get("id", ""))
            name = task.get("name", "")[:28] + (
                ".." if len(task.get("name", "")) > 28 else ""
            )
            status = task.get("status", "")[:10]
            assignee = task.get("assignee", {})
            assignee_name = (assignee.get("username", "") if assignee else "")[:13]
            created = task.get("created_date", "")[:10]

            lines.append(
                f"{tid:<6} {name:<30} {status:<12} {assignee_name:<15} {created:<12}"
            )

        lines.append(separator)
        lines.append(f"Total: {len(tasks)} task(s)")

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

    def _get_all(self, url: str) -> dict:
        all_results = []
        next_url = url

        while next_url:
            response = self.session.get(next_url)
            self._handle_error(response, f"Failed to fetch data from {next_url}")
            data = response.json()

            if "results" not in data:
                return data

            all_results.extend(data["results"])
            next_url = data.get("next")

        return {"results": all_results, "count": len(all_results)}

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
        url = f"{self.api_url}/labels?task_id={task_id}"
        return self._get_all(url).get("results", [])

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

    def list_projects(self) -> dict:
        """List all projects."""
        url = f"{self.api_url}/projects"
        return self._get_all(url)

    def get_project(self, project_id: int) -> dict:
        """Retrieve project details."""
        url = f"{self.api_url}/projects/{project_id}"
        response = self.session.get(url)
        self._handle_error(response, f"Failed to get project {project_id}")
        return response.json()

    def list_project_tasks(self, project_id: int) -> dict:
        """List all tasks for a specific project."""
        url = f"{self.api_url}/tasks?project_id={project_id}"
        return self._get_all(url)

    def export_project(
        self,
        project_id: int,
        output_dir: Path,
        format_name: str,
        save_images: bool = True,
        only_manual: bool = False,
    ) -> None:
        """Export a project's dataset."""
        url = f"{self.api_url}/projects/{project_id}/dataset/export"
        self._trigger_and_download_dataset(url, output_dir, format_name, save_images, only_manual)

    def export_task(
        self,
        task_id: int,
        output_dir: Path,
        format_name: str,
        save_images: bool = True,
        only_manual: bool = False,
    ) -> None:
        """Export a task's dataset."""
        url = f"{self.api_url}/tasks/{task_id}/dataset/export"
        self._trigger_and_download_dataset(url, output_dir, format_name, save_images, only_manual)

    def _trigger_and_download_dataset(
        self,
        url: str,
        output_dir: Path,
        format_name: str,
        save_images: bool,
        only_manual: bool,
    ) -> None:
        params = {"format": format_name, "save_images": save_images}
        if only_manual:
            filter_logic = {"and": [{"==": [{"var": "source"}, "manual"]}]}
            params["filter"] = json.dumps(filter_logic)

        response = self.session.post(url, params=params)
        self._handle_error(response, f"Failed to trigger export at {url}")

        if response.status_code != 202:
            raise Exception(f"Unexpected status code: {response.status_code}\n{response.text}")

        rq_id = response.json().get("rq_id")
        if not rq_id:
            raise Exception("Could not get request ID for export job.")

        job_result = self.wait_for_job(rq_id)
        download_url = job_result.get("result_url")

        if not download_url.startswith(("http://", "https://")):
            download_url = f"{self.base_url}{download_url}"

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        try:
            self._download_file(download_url, str(tmp_path))
            extract_zip(tmp_path, output_dir)
        finally:
            tmp_path.unlink(missing_ok=True)


def _get_api() -> CVATApi:
    load_dotenv()
    return CVATApi(
        os.getenv("CVAT_URL"),
        os.getenv("CVAT_USERNAME"),
        os.getenv("CVAT_PASSWORD"),
    )


@project_app.command("list")
def project_list(
    project_id: Annotated[
        Optional[int], typer.Option("--id", "-i", help="Project ID to list tasks for.")
    ] = None,
    project_ids: Annotated[
        Optional[str], typer.Option("--ids", help="Project IDs (space-separated).")
    ] = None,
) -> None:
    api = _get_api()

    target_ids = []
    if project_id:
        target_ids.append(project_id)
    if project_ids:
        target_ids.extend([int(pid) for pid in project_ids.split()])

    if not target_ids:
        print(TableFormatter.format_projects_table(api.list_projects()))
        return

    for pid in target_ids:
        project_data = api.get_project(pid)
        print(f"\nProject: {project_data.get('name', 'Unknown')} (ID: {pid})")
        tasks_data = api.list_project_tasks(pid)
        print(TableFormatter.format_tasks_table(tasks_data))


@project_app.command("export")
def project_export(
    project_id: Annotated[int, typer.Option("--id", "-i")],
    output_dir: Annotated[Path, typer.Option("--output-dir", "-o")],
    format_name: Annotated[str, typer.Option("--format", "-f")] = "YOLO 1.1",
    images: Annotated[bool, typer.Option("--images/--no-images")] = True,
    only_manual: bool = False,
) -> None:
    _get_api().export_project(
        project_id, output_dir, format_name, images, only_manual
    )
    print(output_dir)


@task_app.command("export")
def task_export(
    output_dir: Annotated[Path, typer.Option("--output-dir", "-o")],
    task_id: Annotated[Optional[int], typer.Option("--id", "-i")] = None,
    task_ids: Annotated[Optional[str], typer.Option("--ids", help="Task IDs.")] = None,
    format_name: Annotated[str, typer.Option("--format", "-f")] = "YOLO 1.1",
    images: Annotated[bool, typer.Option("--images/--no-images")] = True,
    only_manual: bool = False,
) -> None:
    api = _get_api()
    target_ids = []

    if task_id:
        target_ids.append(task_id)
    if task_ids:
        target_ids.extend([int(tid) for tid in task_ids.split()])

    if not target_ids:
        raise ValueError("No Task ID provided. Use --id or --ids.")

    if len(target_ids) == 1:
        api.export_task(target_ids[0], output_dir, format_name, images, only_manual)
        print(output_dir)
        return

    _export_and_concat_tasks(api, target_ids, output_dir, format_name, images, only_manual)
    print(output_dir)


def _export_and_concat_tasks(api, target_ids, output_dir, format_name, images, only_manual):
    """Exports multiple tasks and merges them into a single directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_root = Path(tmpdir)
        task_dirs = []

        for tid in target_ids:
            task_path = tmp_root / f"task_{tid}"
            task_path.mkdir()
            api.export_task(tid, task_path, format_name, images, only_manual)
            task_dirs.append(task_path)

        # Normalize format for Datumaro (e.g., "YOLO 1.1" -> "yolo")
        datum_format = "yolo" if "yolo" in format_name.lower() else "coco"
        concat_datasets(output_dir, task_dirs, datum_format)
    print(output_dir)
