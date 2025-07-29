from pathlib import Path
from sys import exit
import json

import plotly.graph_objects as go
import typer
from typing_extensions import Annotated
from rich.progress import track

app = typer.Typer()


@app.command()
def main(path: Annotated[Path, typer.Argument()], output_dir):
    """
    Function for plotting nicely formatted tables using Plotly
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    files = extract_files(path)

    for f in track(files, description="Plotting counts..."):
        print(f"Processing {f}...")
        plot(f, output_dir)


def plot(f, output_dir):
    """Function to plot counted features as a styled table."""
    f = Path(f)
    outfile = f.stem + ".png"
    output = output_dir / outfile

    # Load JSON contents
    contents = json.loads(f.read_text(encoding="utf-8"))

    # Extract keys and values
    headers = list(contents.keys())
    row = list(contents.values())

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=headers,
                    fill_color="lightskyblue",
                    align="center",
                    font=dict(color="black", size=16),
                    height=40,
                    line_color="darkslategray",
                ),
                cells=dict(
                    values=[[v] for v in row],
                    fill_color="lavender",
                    align="center",
                    font=dict(color="black", size=14),
                    height=30,
                    line_color="gray",
                ),
            )
        ]
    )

    fig.update_layout(
        width=100 * len(headers), height=200, margin=dict(l=20, r=20, t=20, b=20)
    )

    fig.write_image(output, scale=3)


def extract_files(path):
    """Extract files from a given directory."""
    if path.is_dir():
        files = list(path.glob("*.json"))
        return files
    else:
        print(f"{path} is not a directory.")
        exit()


if __name__ == "__main__":
    app()
