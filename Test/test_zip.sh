#!/bin/bash
#
# Script to create a zip file containing source code to run backward compatibility tests: 
# test.zip.
#
# Peter Rochford
# December 19, 2025

# Name of output zip file
ZIPfile="Test.zip"

# Name of file containing file list to include in zip file
LISTfile="../Examples/test_zip_files.txt"

# Check if zip file exists and rename if necessary
if [ -f $ZIPfile ]; then
   # New name to use if file exists
   DateTime=$(date +%Y%m%d_%H%M%S)
   echo $DateTime
   ZIPfileNew="$ZIPfile"_"$DateTime"
   echo "Zip file '$ZIPfile' exists. Renaming to '$ZIPfileNew'."
   mv "$ZIPfile" "$ZIPfileNew"
fi

# Check list file exists
if [[ ! -f $LISTfile ]]; then
   echo "Error: '$LISTfile' not found."
fi

# Build an array of files, expanding any wildcards
files=()
while IFS= read -r pattern; do
   # Skip empty lines and comments
   [[ -z "$pattern" || "$pattern" =~ ^# ]] && continue

   # Use eval to allow wildcard expansion
   eval "matches=( $pattern )"

   # If nothing matched, skip
   if [[ ${#matches[@]} -eq 0 ]]; then
      echo "Warning: Mpattern'$pattern' matched no files."
      continue
   fi

   files+=("${matches[@]}")
done < "$LISTfile"

# If we have files, zip them
if [[ ${#files[@]} -gt 0 ]]; then
   zip "$ZIPfile" "${files[@]}"
else
   echo "No files to add to $ZIPfile."
fi

