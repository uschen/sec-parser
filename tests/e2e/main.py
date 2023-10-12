import json
from pathlib import Path

import click

from sec_parser import Edgar10QParser
from tests.e2e.snapshot import write_snapshot as run_update

DEFAULT_E2E_DATA_DIR = (
    Path(__file__).resolve().parent.parent.parent / "sec-parser-e2e-data"
)


@click.group()
def cli() -> None:
    pass


UPDATE_HELP = (
    "Directory containing cloned repository from alphanome-ai/sec-parser-e2e-data."
)


@click.command()
@click.option("--dir", default=DEFAULT_E2E_DATA_DIR, help=UPDATE_HELP)
def update(path: str) -> None:
    """Update or create semantic-elements-list.json for each primary-document.html."""
    run_update(path)


cli.add_command(update)

if __name__ == "__main__":
    cli()
    cli()