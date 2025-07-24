from pathlib import Path
from sys import exit
from time import sleep

import pandas as pd
from typing_extensions import Annotated
import typer
from rich.progress import track

app = typer.Typer()

@app.command()
def main(path: Annotated[Path, typer.Argument()], p_value_col, fold_change_col, output_dir, split: bool = False):
    """
    Blah blah blah, ill do this later
    """
    # Extract files of interest
    files = extract_files(path)

    # Filter and save to new directory
    filter_(files, p_value_col, fold_change_col, output_dir, split)

def extract_files(path):
    """Utility function to extract files from a provided path."""
    if path.is_dir():
        print(f"Extracting files from {path}")
        exts = ("*.csv", "*.xlsx", "*.tsv")
        files = [p for pat in exts for p in path.glob(pat)]
        return files
    else:
        print(f"{path} is not a directory.")
        exit()

def filter_(files, p_value_col, fold_change_col, output_dir, split):
    """Function for filtering genes."""
    output_dir = Path(output_dir)
    for f in track(files, description="Filtering..."):
        try:
            df = pd.read_excel(f, engine="openpyxl")
        except Exception as e:
            print(f"Error reading the Excel file {f}: {e}")
            print("Trying csv instead.")
            try:
                df = pd.read_csv(f)
            except Exception as e:
                print(f"Error loading as csv, please check {f} file type.\nException: {e}")
                return

        # Check to make sure columns exist
        if p_value_col not in df.columns or fold_change_col not in df.columns:
            print(f"{p_value_col} or {fold_change_col} not found in {f}.")
            return

        # Filter given fold changes and p-value
        if split:
            split_(f=f, df=df, fold_change_col=fold_change_col, p_value_col=p_value_col, output_dir=output_dir)
        else:
            combined(f=f, df=df, fold_change_col=fold_change_col, p_value_col=p_value_col, output_dir=output_dir)
        
        sleep(0.25)

def combined(f, df, fold_change_col, p_value_col, output_dir):
    # Filter given fold changes and p-value
    try:
        cond = ((df[fold_change_col] < -1) | (df[fold_change_col] > 1)) & (df[p_value_col] < 0.05)
        combined_df = df[cond]
    except Exception as e:
        print(f"Error processing {f}: {e}")

    # Create output files
    combined_ = Path(f)

    combined_ = "combined_" + combined_.name
    output_dir.mkdir(parents=True, exist_ok=True)

    combined_path = output_dir / combined_
    combined_df.to_csv(combined_path, index=False)
    print(f"Filtered data {combined_} exported to {output_dir}.")

def split_(f, df, fold_change_col, p_value_col, output_dir):
    # Filter given fold changes and p-value
    try:
        upregulated_df = df[(df[fold_change_col] > 1) & (df[p_value_col] < 0.05)]
        downregulated_df = df[(df[fold_change_col] < -1) & (df[p_value_col] < 0.05)]
    except Exception as e:
        print(f"Error processing {f}: {e}")

    # Create output files
    up = Path(f)
    down = Path(f)

    up = "upregulated_" + up.name
    down = "downgreglated_" + down.name
    output_dir.mkdir(parents=True, exist_ok=True)

    up_path = output_dir / up
    down_path = output_dir / down

    upregulated_df.to_csv(up_path, index=False)
    downregulated_df.to_csv(down_path, index=False)
    print(f"Filtered data {up} and {down} exported to {output_dir}.")

if __name__ == "__main__":
    app()