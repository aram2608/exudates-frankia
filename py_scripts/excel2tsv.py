from pathlib import Path
from typing_extensions import Annotated

import pandas as pd
import typer
from rich.progress import track

app = typer.Typer()

@app.command()
def excel_to_csv(input_dir: Annotated[Path, typer.Argument()], output_dir):
    # Prompt user for multiple Excel file names
    files = get_files(input_dir)
    output = Path(output_dir)
    
    # Loop through each Excel file and convert to CSV
    for f in track(files, description="Converting to csv..."):
        excel = Path(f)
        # Read the Excel file
        df = pd.read_excel(f)

        csv = excel.stem + ".csv"
        out = output / csv
        output.mkdir(parents=True, exist_ok=True)
        df.to_csv(out, index=False)
        print(f"Converted {excel} to {csv}")

def get_files(path):
    """Function used to extract files from input directory."""
    if path.is_dir():
        print(f"Extracting files from {path}...")
        files = list(path.glob("*.xlsx"))
        return files
    else:
        print(f"{path} is not a directory")
        exit()

# Run the conversion function
if __name__ == "__main__":
    app()