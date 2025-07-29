from pathlib import Path
import argparse
import time
from Bio import Entrez
import pandas as pd

# Set your email to comply with NCBI usage policies
Entrez.email = "ja1473@usnh.edu"  # Change to your email


def read_protein_aids(tsv_file, column_name):
    """
    Reads protein accession IDs from a CSV file.
    """ 
    df = pd.read_csv(tsv_file)
    protein_aids = df[column_name]
    return protein_aids


def fetch_protein_sequence(protein_aid, retries=3):
    """
    Queries NCBI for a protein sequence using an accession ID.
    """
    for attempt in range(retries):
        try:
            handle = Entrez.efetch(
                db="protein", id=protein_aid, rettype="fasta", retmode="text"
            )
            fasta_data = handle.read()
            handle.close()
            return fasta_data
        except Exception as e:
            print(f"Error fetching {protein_aid} (attempt {attempt+1}): {e}")
            time.sleep(2**attempt)
    return None


def write_fasta(output_file, sequences):
    """
    Writes sequences to a FASTA file.
    """
    with open(output_file, "w") as file:
        for sequence in sequences:
            file.write(sequence + "\n")

def extract_files(path):
    """Utility function to extract files from a provided path."""
    path = Path(path)
    if path.is_dir():
        print(f"Extracting files from {path}")
        exts = ("*.csv", "*.xlsx", "*.tsv")
        files = [p for pat in exts for p in path.glob(pat)]
        return files
    else:
        print(f"{path} is not a directory.")
        exit()

def main(path, output_path, column_index=0, delay=0.35):
    """
    Main function to process the TSV file and fetch sequences.

    :param tsv_file: Input TSV file containing protein AIDs.
    :param output_fasta: Output FASTA file.
    :param column_index: Column index for accession IDs in TSV.
    :param delay: Delay between API requests to avoid throttling (default: 0.35s).
    """
    files = extract_files(path)
    for f in files:
        protein_aids = read_protein_aids(f, column_index)
        print(f"Found {len(protein_aids)} protein AIDs.")

        sequences = []
        for idx, protein_aid in enumerate(protein_aids):
            print(f"[{idx+1}/{len(protein_aids)}] Fetching: {protein_aid}")
            sequence = fetch_protein_sequence(protein_aid)
            if sequence:
                sequences.append(sequence)
            else:
                print(f"Warning: No data retrieved for {protein_aid}")

            # Enforce rate limit (max 3 requests/sec)
            time.sleep(delay)

        f = Path(f)
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        output_fasta = output_path / f.stem

        write_fasta(output_fasta, sequences)
        print(f"\nFASTA file saved: {output_fasta}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch protein sequences from NCBI and save to a FASTA file."
    )
    parser.add_argument("tsv_file", help="Input TSV file with protein accession IDs.")
    parser.add_argument("output_fasta", help="Output FASTA file.")
    parser.add_argument(
        "--column",
        type=str,
        help="Column name for protein IDs",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.35,
        help="Delay between requests to NCBI (default: 0.35s for 3 requests/sec).",
    )

    args = parser.parse_args()
    main(args.tsv_file, args.output_fasta, args.column, args.delay)
