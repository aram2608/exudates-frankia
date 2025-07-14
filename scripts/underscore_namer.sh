#!/bin/bash

DIR=$1
OUT=$2

if [ ! -d "$DIR" ] || [ ! -d "$OUT" ]; then
    echo "Usage: $0 input/dir/ output/dir/"
    exit 1
fi

for file in $DIR/*; do
    if [ -f "$file" ]; then
        base_name=$(basename "$file")
        new_file="${base_name// /_}"

        echo "Moving $new_file to $OUT..."
        mv $DIR/"$base_name" "$OUT/$new_file"

        if [ $? -ne 0 ]; then
            echo "Failed moving $new_file."
        else
            echo "Success."
        fi
    else
        echo "$file is not a file."
    fi
echo "Done renaming $DIR"
done