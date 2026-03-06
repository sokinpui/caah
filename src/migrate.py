import concurrent.futures
import os
import tempfile
from pathlib import Path
from typing import Annotated, Optional

import typer
from cvat_sdk import make_client
from cvat_sdk.api_client import models
from cvat_sdk.core.proxies.tasks import ResourceType
from dotenv import load_dotenv

from utils import CONTEXT_SETTINGS

migrate_app = typer.Typer(
    help="Migration tools for moving tasks between servers.",
    context_settings=CONTEXT_SETTINGS,
)


def _get_migration_config():
    """Helper to load credentials for both source and target servers."""
    load_dotenv()
    target = (
        os.getenv("CVAT_USERNAME"),
        os.getenv("CVAT_PASSWORD"),
        os.getenv("CVAT_URL"),
    )
    source = (
        os.getenv("CVAT_USERNAME_2"),
        os.getenv("CVAT_PASSWORD_2"),
        os.getenv("CVAT_URL_2"),
    )

    if not all(target):
        raise ValueError("Target CVAT credentials missing in .env (CVAT_URL, etc.)")
    if not all(source):
        raise ValueError("Source CVAT credentials missing in .env (CVAT_URL_2, etc.)")

    return source, target


def _clone_labels(labels) -> list[models.PatchedLabelRequest]:
    """Converts existing labels to request models, stripping IDs."""
    new_labels = []
    for label in labels:
        label_dict = label.to_dict()
        label_dict.pop("id", None)
        if "attributes" in label_dict:
            for attr in label_dict["attributes"]:
                attr.pop("id", None)
        new_labels.append(models.PatchedLabelRequest(**label_dict))
    return new_labels


def _migrate_task_worker(
    task_id: int,
    source_config: tuple,
    target_config: tuple,
    project_id: Optional[int] = None,
) -> str:
    """
    Worker function to migrate a single task.
    Opens fresh client connections for thread safety.
    """
    (source_user, source_pass, source_url) = source_config
    (target_user, target_pass, target_url) = target_config

    try:
        with make_client(
            source_url, credentials=(source_user, source_pass)
        ) as source_client, make_client(
            target_url, credentials=(target_user, target_pass)
        ) as target_client:

            old_task = source_client.tasks.retrieve(task_id)
            new_task = _migrate_task_internal(old_task, target_client, project_id)

            if not new_task:
                return f"[SKIPPED] Task {task_id}: No data found."

            return (
                f"[SUCCESS] Migrated task: {old_task.name} "
                f"({task_id} -> {new_task.id})"
            )
    except Exception as e:
        return f"[ERROR] Failed to migrate task {task_id}: {str(e)}"


def _migrate_task_internal(old_task, new_client, project_id: Optional[int] = None):
    """Core logic to migrate a single task instance using NAS sharing."""
    meta = old_task.get_meta()
    server_files = [frame.name for frame in meta.frames]

    if not server_files:
        print(
            f"Skipping task '{old_task.name}' (ID: {old_task.id}): No image data found."
        )
        return None

    task_data = {"name": old_task.name, "project_id": project_id}

    if not project_id:
        task_data["labels"] = _clone_labels(old_task.get_labels())

    task_request = models.TaskWriteRequest(**task_data)
    new_task = new_client.tasks.create(task_request)

    new_task.upload_data(
        resources=server_files,
        resource_type=ResourceType.SHARE,
        params={"image_quality": 100},
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        annotation_path = Path(tmpdir) / "annotations.zip"

        old_task.export_dataset(
            "CVAT for images 1.1", str(annotation_path), include_images=False
        )

        if annotation_path.exists():
            new_task.import_annotations("CVAT 1.1", str(annotation_path))

    return new_task


@migrate_app.command("task")
def migrate_task(
    task_id: Annotated[
        int, typer.Option("--task-id", "-t", help="Task ID on the old server.")
    ],
    project_id: Annotated[
        Optional[int],
        typer.Option("--project-id", "-p", help="Target Project ID on the NEW server."),
    ] = None,
) -> None:
    """Migrates a single task from old server to new server."""
    (
        (source_user, source_pass, source_url),
        (target_user, target_pass, target_url),
    ) = _get_migration_config()

    print(f"Migrating task {task_id} from {source_url} to {target_url}...")

    with make_client(
        source_url, credentials=(source_user, source_pass)
    ) as old_client, make_client(
        target_url, credentials=(target_user, target_pass)
    ) as new_client:

        old_task = old_client.tasks.retrieve(task_id)
        new_task = _migrate_task_internal(old_task, new_client, project_id)

        if new_task:
            print(f"Successfully migrated task {task_id} -> {new_task.id}")


@migrate_app.command("tasks")
def migrate_tasks(
    include_orphans: Annotated[
        bool, typer.Option("--orphans", help="Migrate tasks not assigned to a project.")
    ] = True,
    jobs: Annotated[
        int, typer.Option("--jobs", "-j", help="Number of parallel migrations.")
    ] = 2,
) -> None:
    """Migrates all tasks from source to target, matching or creating projects by name."""
    (
        (source_user, source_pass, source_url),
        (target_user, target_pass, target_url),
    ) = _get_migration_config()

    with make_client(
        source_url, credentials=(source_user, source_pass)
    ) as old_client, make_client(
        target_url, credentials=(target_user, target_pass)
    ) as new_client:

        target_projects = new_client.projects.list()
        project_map = {p.name: p.id for p in target_projects}

        source_projects = old_client.projects.list()
        all_tasks_to_migrate = []  # List of (task_id, target_project_id)
        all_source_tasks = old_client.tasks.list()

        for sp in source_projects:
            target_id = project_map.get(sp.name)

            if not target_id:
                print(f"Project '{sp.name}' not found on target. Creating layout...")
                new_labels = _clone_labels(sp.get_labels())
                project_req = models.ProjectWriteRequest(
                    name=sp.name, labels=new_labels
                )
                created_proj = new_client.projects.create(project_req)
                target_id = created_proj.id
                project_map[sp.name] = target_id

            project_tasks = [t for t in all_source_tasks if t.project_id == sp.id]
            for t in project_tasks:
                all_tasks_to_migrate.append((t.id, target_id))

        if include_orphans:
            orphan_tasks = [t for t in all_source_tasks if t.project_id is None]
            for t in orphan_tasks:
                all_tasks_to_migrate.append((t.id, None))

    if not all_tasks_to_migrate:
        print("No tasks found to migrate.")
        return

    print(f"Starting migration of {len(all_tasks_to_migrate)} tasks using {jobs} jobs...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        futures = [
            executor.submit(_migrate_task_worker, tid, (source_user, source_pass, source_url), (target_user, target_pass, target_url), pid)
            for tid, pid in all_tasks_to_migrate
        ]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())


@migrate_app.command("project-layout")
def migrate_project_layout(
    project_id: Annotated[
        Optional[int],
        typer.Option(
            "--project-id",
            "-p",
            help="Specific Project ID to migrate. If omitted, migrates ALL.",
        ),
    ] = None,
) -> None:
    """Creates projects on the target server with the same names and labels as the source."""
    (
        (source_user, source_pass, source_url),
        (target_user, target_pass, target_url),
    ) = _get_migration_config()

    print(f"Syncing project layouts from {source_url} to {target_url}...")

    with make_client(
        source_url, credentials=(source_user, source_pass)
    ) as old_client, make_client(
        target_url, credentials=(target_user, target_pass)
    ) as new_client:

        if project_id:
            source_projects = [old_client.projects.retrieve(project_id)]
        else:
            source_projects = old_client.projects.list()

        for sp in source_projects:
            print(f"Processing project: {sp.name} (ID: {sp.id})...")
            new_labels = _clone_labels(sp.get_labels())

            project_request = models.ProjectWriteRequest(
                name=sp.name,
                labels=new_labels,
            )

            created = new_client.projects.create(project_request)
            print(
                f"Created project '{created.name}' with ID {created.id} on target server."
            )

    print("Project layout migration complete.")
