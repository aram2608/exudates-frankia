#!/bin/bash

# This script searches for a gene in a TSV file and returns the corresponding line.
# Usage: ./gene_search.sh <gene_name> <file.tsv>
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <gene_name> <file.tsv>"
    exit 1
fi
GENE_NAME1=$1
FILE=$2
if [ ! -f "$FILE" ]; then
    echo "File not found!"
    exit 1
fi
# Search for the gene name in the TSV file and print the corresponding line
grep "\t$GENE_NAME1\t" "$FILE" >> GOI.txt
# Note: The script assumes that the TSV file has tab-separated values and that the gene name is in the second column.
# Adjust the grep command if the gene name is in a different column.
# Example usage:
# ./gene_search.sh BRCA1 genes.tsv
