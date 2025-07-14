#!/bin/bash
# Renames files in DIR by replacing spaces with underscores and moves them to OUT.

DIR=$1
OUT=$2
MODE=$3

# Removes first trailing slash if present
DIR="${DIR%/}"
OUT="${OUT%/}"

# Main function for renaming files
function rename() {
    for file in "$DIR"/*; do
        if [ -f "$file" ]; then
            # Extracts the basename and removes spaces
            base_name=$(basename "$file")
            new_file="${base_name// /_}"

            echo "Moving $base_name to $OUT/$new_file..."
            if mv "$file" "$OUT/$new_file"; then
                echo "Success."
            else
                echo "Failed moving $new_file."
            fi
        else
            echo "$file is not a file."
        fi
    done
    echo "Done renaming $DIR"
}

# Dry run function to see example output
function dry() {
    for file in "$DIR"/*; do
        if [ -f "$file" ]; then
            base_name=$(basename "$file")
            new_file="${base_name// /_}"

            echo "[Dry run] Would move $base_name to $OUT/$new_file"
        else
            echo "$file is not a file."
        fi
    done
    echo "Dry run complete for $DIR"
}

if [ ! -d "$DIR" ] || [ ! -d "$OUT" ]; then
    echo "Usage: $0 input/dir/ output/dir/ --run"
    echo "Optional: --dry for a dry run"
    exit 1
fi

# Create output directory if it does not exist
mkdir -p "$OUT"

if [[ "$MODE" == "--dry" ]]; then
    dry
elif [[ "$MODE" == "--run" ]]; then
    rename
else
    echo "Unexpected argument: $MODE"
    echo "Try --dry or --run instead"
    exit 1
fi

exit 0