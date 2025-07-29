from pathlib import Path
from time import sleep

import pandas as pd  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns  # type: ignore
import typer
from rich.progress import track
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def main(
    file_path: Annotated[Path, typer.Argument()],
    column_name,
    out_path: Annotated[Path, typer.Option("-o")],
    excel: bool = False,
    tsv: bool = False,
):
    sns.set(style="whitegrid")

    files = extract_files(file_path)

    for f in track(files, description="Plotting pie charts..."):
        if excel:
            df = pd.read_excel(f)
        elif tsv:
            df = pd.read_csv(f, delimiter="\t")
        else:
            df = pd.read_csv(f)
        value_counts = df[column_name].value_counts()

        # Create figure and axis for pie chart
        fig, ax = plt.subplots(figsize=(6, 6), facecolor="none")

        # Generate colors
        cmap = plt.get_cmap("tab20")
        colors = [cmap(i) for i in range(len(value_counts))]

        # Plot pie chart without labels or autopct
        wedges, texts = ax.pie(
            value_counts,
            labels=None,
            colors=colors,
            startangle=140,
            textprops={"fontsize": 10},
        )
        #ax.set_title("BGC Product Distribution", fontsize=12)
        ax.axis("equal")

        # Save output file
        out_path.mkdir(parents=True, exist_ok=True)
        file = f.stem + ".png"
        legend = f.stem + "_legend.png"
        outfile = out_path / file
        legend = out_path / legend
        plt.savefig(outfile, bbox_inches="tight", transparent=True)
        plt.close()

        # Create legend for output
        labels = [f"{label} ({count} matches)" for label, count in value_counts.items()]

        fig, ax = plt.subplots(figsize=(3.5, len(labels) * 0.3), facecolor="none")
        handles = [
            plt.Line2D(
                [0], [0], marker="o", color="w", markerfacecolor=color, markersize=10
            )
            for color in colors
        ]
        ax.legend(
            handles,
            labels,
            title="BGC Products",
            loc="center",
            frameon=False,
            fontsize=10,
            title_fontsize=11,
        )
        ax.axis("off")
        plt.savefig(legend, bbox_inches="tight", transparent=True)
        plt.close()
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


if __name__ == "__main__":
    app()
