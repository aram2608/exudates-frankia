from pathlib import Path
from sys import exit
from time import sleep
import json

import pandas as pd
import typer
from typing_extensions import Annotated
from rich.progress import track

app = typer.Typer()


@app.command()
def main(path: Annotated[Path, typer.Argument()], column, output_dir):
    """
    Utility script to count the occurences of a feature in a csv file.
    """
    files = extract_files(path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for f in track(files, description="Counting features..."):
        process(f, column, output_dir)
        sleep(0.25)


def extract_files(path):
    """Function to extract files from a directory."""
    if path.is_dir():
        print(f"Extracting files from {path}...")
        files = list(path.glob("*.csv"))
        return files
    else:
        print(f"{path} is not a directory.")
        exit()


def process(f, column, output_dir):
    """Count the features for each column and export a JSON."""
    print(f"Processing {f}")
    f = Path(f)
    df = pd.read_csv(f)
    counts = df[column].value_counts()
    counts.to_json((output_dir / f"{f.name}.json"))
    sleep(0.25)


if __name__ == "__main__":
    app()
