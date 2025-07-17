import os
from sys import exit
from pathlib import Path

import pandas as pd
from Bio import SeqIO
import typer
from typing_extensions import Annotated
from rich.progress import track

app = typer.Typer()


@app.command()
def main(
    path: Annotated[Path, typer.Argument()],
    locus_tag_column,
    antismash_file,
    output_dir,
):
    """
    Usage blah blah blah
    """

    # Convert BGC list to a DataFrame
    bgc_data = extract_bgs(antismash_file)

    # Get all files from directory
    files = get_files(path)

    # Process each file in directory
    for f in track(files, description="Processing file..."):
        process_file(f, locus_tag_column, bgc_data, output_dir)


def process_file(f, locus_tag_column, bgc_data, output_dir):
    output_dir = Path(output_dir)
    try:
        rna_seq_data = pd.read_excel(f, engine="openpyxl")
    except Exception as e:
        print(f"Error reading the Excel file {f}: {e}")
        print("Trying csv instead.")
        try:
            rna_seq_data = pd.read_csv(f)
        except Exception as e:
            print(f"Error loading as csv, please check {f} file type.\nException: {e}")
            return

    # Verify if the specified column exists
    if locus_tag_column not in rna_seq_data.columns:
        print(f"The specified column '{locus_tag_column}' does not exist in {f}.")
        return

    # Match the genes based on the specified locus tag column without any significance filter
    merged_data = pd.merge(
        rna_seq_data,
        bgc_data,
        how="inner",
        left_on=locus_tag_column,
        right_on="locus_tag",
    )

    # Export the matched data to an Excel file with "BGC" appended to the file name
    if not merged_data.empty:
        f = Path(f)
        output_dir.mkdir(parents=True, exist_ok=True)
        out_file = f.stem + "_BGC.csv"
        full_path = output_dir / out_file

        # Write and report
        merged_data.to_csv(full_path, index=False)
        print(f"Matched data exported to {full_path}")
    else:
        print("No matching genes found.")


def extract_bgs(antismash_file):
    # Parsing the GenBank file to collect BGC data
    bgc_list = []

    # Parse the GenBank file
    for record in SeqIO.parse(antismash_file, "genbank"):
        # Iterate through features in the GenBank file
        for feature in record.features:
            # Check if the feature is a CDS and has a 'locus_tag'
            if feature.type == "CDS" and "locus_tag" in feature.qualifiers:
                locus_tag = feature.qualifiers["locus_tag"][0]

                # Iterate through features again to find BGCs
                for bgc_feature in record.features:
                    # Check if the feature is a BGC region
                    if (
                        bgc_feature.type == "region"
                        and "product" in bgc_feature.qualifiers
                    ):
                        # Check if the CDS is within the BGC region
                        if (
                            feature.location.start >= bgc_feature.location.start
                            and feature.location.end <= bgc_feature.location.end
                        ):
                            # Create a dictionary to store BGC information
                            bgc_info = {
                                "locus_tag": locus_tag,
                                "BGC_Product": bgc_feature.qualifiers.get(
                                    "product", ["Unknown"]
                                )[0],
                                "BGC_Start": bgc_feature.location.start,
                                "BGC_End": bgc_feature.location.end,
                            }
                            bgc_list.append(bgc_info)

    # Convert BGC list to a DataFrame
    bgc_data = pd.DataFrame(bgc_list)
    if not bgc_data.empty:
        return bgc_data
    else:
        print("Failed to extract BGC's")
        exit()


def get_files(path):
    if path.is_dir():
        print(f"Extracting files from {path}...")
        files = list(path.glob("*.csv" or "*.xlsx"))
        return files
    else:
        print(f"{path} is not a directory")
        exit()


if __name__ == "__main__":
    app()
