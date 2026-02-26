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
