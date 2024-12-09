#!/bin/bash

# Loop through all files ending with .pdf.PROCESSED
for file in *.pdf.PROCESSED; do
    # Check if there are any matching files
    if [ -e "$file" ]; then
        # Extract the base name by removing .PROCESSED
        newname="${file%.PROCESSED}"
        # Rename the file
        mv "$file" "$newname"
        echo "Renamed: $file -> $newname"
    fi
done
