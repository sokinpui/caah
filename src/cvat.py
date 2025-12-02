import argparse
import os
import shutil
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


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
            print("Successfully logged in to CVAT.")
        except requests.exceptions.RequestException as e:
            print(f"Login failed: {e}")
            if e.response is not None:
                print(f"Response: {e.response.text}")
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

    def _download_file(self, url, output_path):
        """Download a file with streaming."""
        print(f"Downloading from {url} to {output_path}...")
        with self.session.get(url, stream=True) as r:
            self._handle_error(r, "File download failed")
            with open(output_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        print("Download complete.")

    # --- Project Operations ---

    def create_project(self, name):
        """Create a new project."""
        url = f"{self.api_url}/projects"
        response = self.session.post(url, json={"name": name})
        self._handle_error(response, f"Failed to create project '{name}'")
        project_data = response.json()
        print(f"Successfully created project '{name}' with ID: {project_data['id']}")
        return project_data

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
            print("Project import job finished.")
        else:
            print("Project import started.")

    # --- Task Operations ---

    def create_task(self, name, project_id, image_paths):
        """Create a new task and upload images."""
        url = f"{self.api_url}/tasks"
        payload = {"name": name}
        if project_id:
            payload["project_id"] = project_id

        response = self.session.post(url, json=payload)
        self._handle_error(response, f"Failed to create task '{name}'")
        task_id = response.json()["id"]
        print(f"Successfully created task '{name}' with ID: {task_id}")

        data_url = f"{self.api_url}/tasks/{task_id}/data"
        files_to_upload = []
        try:
            for p in image_paths:
                files_to_upload.append(("client_files", open(p, "rb")))

            data = {"image_quality": 70}
            response = self.session.post(data_url, data=data, files=files_to_upload)
            self._handle_error(response, f"Failed to upload images to task {task_id}")
            print(f"Successfully uploaded {len(image_paths)} images to task {task_id}.")
        finally:
            for _, f in files_to_upload:
                f.close()

    def backup_task(self, task_id, output_file):
        """Backup a task."""
        url = f"{self.api_url}/tasks/{task_id}/backup/export"
        response = self.session.post(url)
        self._handle_error(response, f"Failed to trigger backup for task {task_id}")

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

    def import_task(self, backup_file):
        """Import a task from a backup."""
        url = f"{self.api_url}/tasks/backup"
        with open(backup_file, "rb") as f:
            files = {"task_file": (Path(backup_file).name, f, "application/zip")}
            response = self.session.post(url, files=files)
        self._handle_error(response, f"Failed to import task from {backup_file}")

        if response.status_code == 202:
            rq_id = response.json().get("rq_id")
            self.wait_for_job(rq_id)
            print("Task import job finished.")
        else:
            print("Task import started.")

    def export_task(self, task_id, output_file, format_name):
        """Export a task's dataset."""
        url = f"{self.api_url}/tasks/{task_id}/dataset/export"
        params = {"format": format_name}
        payload = {"save_images": True}
        response = self.session.post(url, params=params, json=payload)
        self._handle_error(response, f"Failed to trigger export for task {task_id}")

        rq_id = None
        if response.status_code == 202:  # Asynchronous
            rq_id = response.json().get("rq_id")
        elif response.status_code != 201:  # Not sync and not async
            self._handle_error(
                response, f"Unexpected status code for export trigger"
            )

        if rq_id:
            self.wait_for_job(rq_id)

        download_url = f"{self.api_url}/tasks/{task_id}/dataset/export"
        download_params = {"action": "download"}
        print(f"Downloading from {download_url} with params {download_params}...")
        with self.session.get(download_url, params=download_params, stream=True) as r:
            self._handle_error(r, "Dataset download failed")
            with open(output_file, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        print(f"Download complete. Saved to {output_file}")

    def upload_annotations(self, task_id, annotations_file, format_name):
        """Upload annotations to a task."""
        url = f"{self.api_url}/tasks/{task_id}/annotations"
        params = {"format": format_name}

        with open(annotations_file, "rb") as f:
            files = {"annotation_file": (Path(annotations_file).name, f)}
            response = self.session.put(url, params=params, files=files)

        self._handle_error(response, f"Failed to upload annotations for task {task_id}")

        if response.status_code == 202:  # Asynchronous
            rq_id = response.json().get("rq_id")
            if not rq_id:
                raise Exception("Could not get request ID for annotation upload job.")
            self.wait_for_job(rq_id)
            print("Annotation upload job finished.")
        elif response.status_code == 201:  # Synchronous
            print("Annotations uploaded successfully.")


def main():
    """Main function to run the CVAT API client."""
    load_dotenv()

    parser = argparse.ArgumentParser(description="CVAT REST API client.")
    subparsers = parser.add_subparsers(dest="resource", required=True)

    # Project parser
    project_parser = subparsers.add_parser("project", help="Project operations")
    project_subparsers = project_parser.add_subparsers(dest="action", required=True)
    p_create = project_subparsers.add_parser("create", help="Create a project")
    p_create.add_argument("--name", required=True, help="Name of the project")
    p_backup = project_subparsers.add_parser("backup", help="Backup a project")
    p_backup.add_argument("--id", required=True, type=int, help="Project ID")
    p_backup.add_argument("--output-file", required=True, help="Path to save backup")
    p_import = project_subparsers.add_parser("import", help="Import a project")
    p_import.add_argument("--input-file", required=True, help="Path to backup zip")

    # Task parser
    task_parser = subparsers.add_parser("task", help="Task operations")
    task_subparsers = task_parser.add_subparsers(dest="action", required=True)
    t_create = task_subparsers.add_parser("create", help="Create a task")
    t_create.add_argument("--name", required=True, help="Name of the task")
    t_create.add_argument("--project-id", type=int, help="Project ID to associate with")
    t_create.add_argument("--images", nargs="+", required=True, help="Paths to images")
    t_backup = task_subparsers.add_parser("backup", help="Backup a task")
    t_backup.add_argument("--id", required=True, type=int, help="Task ID")
    t_backup.add_argument("--output-file", required=True, help="Path to save backup")
    t_import = task_subparsers.add_parser("import", help="Import a task")
    t_import.add_argument("--input-file", required=True, help="Path to backup zip")
    t_export = task_subparsers.add_parser("export", help="Export a task dataset")
    t_export.add_argument("--id", required=True, type=int, help="Task ID")
    t_export.add_argument("--output-file", required=True, help="Path to save dataset")
    t_export.add_argument("--format", required=True, help="Export format name")
    t_upload = task_subparsers.add_parser(
        "upload_annotations", help="Upload annotations to a task"
    )
    t_upload.add_argument("--id", required=True, type=int, help="Task ID")
    t_upload.add_argument("--input-file", required=True, help="Path to annotations file")
    t_upload.add_argument(
        "--format", required=True, help="Annotation format name (e.g., 'CVAT 1.1')"
    )

    args = parser.parse_args()

    try:
        api = CVATApi(
            os.getenv("CVAT_URL"),
            os.getenv("CVAT_USERNAME"),
            os.getenv("CVAT_PASSWORD"),
        )

        if args.resource == "project":
            if args.action == "create":
                api.create_project(args.name)
            elif args.action == "backup":
                api.backup_project(args.id, args.output_file)
            elif args.action == "import":
                api.import_project(args.input_file)
        elif args.resource == "task":
            if args.action == "create":
                api.create_task(args.name, args.project_id, args.images)
            elif args.action == "backup":
                api.backup_task(args.id, args.output_file)
            elif args.action == "import":
                api.import_task(args.input_file)
            elif args.action == "export":
                api.export_task(args.id, args.output_file, args.format)
            elif args.action == "upload_annotations":
                api.upload_annotations(args.id, args.input_file, args.format)
    except (requests.exceptions.RequestException, ValueError, Exception) as e:
        print(f"An operation failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
