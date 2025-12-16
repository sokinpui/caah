import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml


def setup_data_parser(parser):
    """Adds data utility subcommands to the parser."""
    subparsers = parser.add_subparsers(
        dest="action", required=True, help="Available data commands"
    )

    unpick_parser = subparsers.add_parser(
        "unpick", help="Separate manual and auto annotations into different datasets."
    )
    unpick_parser.set_defaults(func=run_unpick)


def run_unpick(args):
    """Separates manual and auto annotations into two zip files."""
    input_zip = Path(args.input)
    manual_zip = Path(args.manual_output)
    auto_zip = Path(args.auto_output)

    if not input_zip.is_file():
        print(f"Error: Input file not found: {input_zip}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        source_dir = tmpdir_path / "source"
        manual_dir = tmpdir_path / "manual"
        auto_dir = tmpdir_path / "auto"

        source_dir.mkdir()
        manual_dir.mkdir()
        auto_dir.mkdir()

        print(f"Extracting {input_zip.name}...", file=sys.stderr)
        with zipfile.ZipFile(input_zip, "r") as zip_ref:
            zip_ref.extractall(source_dir)

        # 1. Parse data.yaml to build mappings
        yaml_files = list(source_dir.glob("**/data.yaml"))
        if not yaml_files:
            print("Error: data.yaml not found in dataset.", file=sys.stderr)
            sys.exit(1)

        original_yaml_path = yaml_files[0]
        with open(original_yaml_path, "r") as f:
            data_config = yaml.safe_load(f)

        names_obj = data_config.get("names", [])
        # Normalize to dict {id: name}
        if isinstance(names_obj, list):
            original_names = {i: n for i, n in enumerate(names_obj)}
        elif isinstance(names_obj, dict):
            original_names = {int(k): v for k, v in names_obj.items()}
        else:
            print("Error: Unknown format for 'names' in data.yaml", file=sys.stderr)
            sys.exit(1)

        manual_names = []
        auto_names = []
        map_manual = {}  # old_id -> new_id
        map_auto = {}  # old_id -> new_id

        for idx, name in sorted(original_names.items()):
            if name.endswith(" (auto)"):
                map_auto[idx] = len(auto_names)
                auto_names.append(name)
            else:
                map_manual[idx] = len(manual_names)
                manual_names.append(name)

        print(
            f"Found {len(manual_names)} manual classes and {len(auto_names)} auto classes.",
            file=sys.stderr,
        )

        # 2. Process files
        # We walk through source_dir.
        # Images: copy to both.
        # Labels: split and rewrite.
        # Other (yaml): handle separately.

        for item in source_dir.rglob("*"):
            if not item.is_file():
                continue

            rel_path = item.relative_to(source_dir)

            # Skip the original yaml, we will create new ones
            if item.name == "data.yaml":
                continue

            suffix = item.suffix.lower()

            # Prepare destinations
            m_dest = manual_dir / rel_path
            a_dest = auto_dir / rel_path
            m_dest.parent.mkdir(parents=True, exist_ok=True)
            a_dest.parent.mkdir(parents=True, exist_ok=True)

            if suffix == ".txt" and "labels" in item.parts:
                # Process Label File
                with open(item, "r") as f:
                    lines = f.readlines()

                m_lines = []
                a_lines = []

                for line in lines:
                    parts = line.strip().split()
                    if not parts:
                        continue
                    try:
                        cls_id = int(parts[0])
                        rest = " ".join(parts[1:])
                        if cls_id in map_manual:
                            m_lines.append(f"{map_manual[cls_id]} {rest}\n")
                        if cls_id in map_auto:
                            a_lines.append(f"{map_auto[cls_id]} {rest}\n")
                    except ValueError:
                        pass  # Skip invalid lines

                if m_lines:
                    with open(m_dest, "w") as f:
                        f.writelines(m_lines)
                if a_lines:
                    with open(a_dest, "w") as f:
                        f.writelines(a_lines)
            else:
                # Copy Image or other file (e.g. README)
                shutil.copy2(item, m_dest)
                shutil.copy2(item, a_dest)

        # 3. Create new data.yaml files
        def write_yaml(path, names_list):
            # Use relative paths common in YOLO structure
            # Assuming standard structure exists, else reuse source keys if possible?
            # Safest is to reuse source config but replace names/nc
            new_config = data_config.copy()
            new_config["names"] = names_list
            new_config["nc"] = len(names_list)
            with open(path, "w") as f:
                yaml.dump(new_config, f, sort_keys=False)

        write_yaml(manual_dir / "data.yaml", manual_names)
        write_yaml(auto_dir / "data.yaml", auto_names)

        # 4. Zip results
        print(f"Creating manual zip at {manual_zip}...", file=sys.stderr)
        shutil.make_archive(str(manual_zip.with_suffix("")), "zip", manual_dir)

        print(f"Creating auto zip at {auto_zip}...", file=sys.stderr)
        shutil.make_archive(str(auto_zip.with_suffix("")), "zip", auto_dir)

    print(f"{manual_zip}\n{auto_zip}")
