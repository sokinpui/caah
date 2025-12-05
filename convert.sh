#!/bin/bash

# Create a directory for the output
mkdir -p output_md

# Read the file line by line
while read -r url; do
  # 1. Generate a filename from the URL
  # Removes trailing slash first (${url%/}), then grabs the last segment (basename)
  filename=$(basename "${url%/}")

  echo "Processing: $filename"

  # 2. Fetch with wget2 and Pipe to Pandoc
  # -O -  : tells wget2 to write to Standard Output (stdout) instead of a file
  # -q    : quiet mode (hides wget progress bars)
  # -f html -t gfm : Convert From HTML To GitHub-Flavored Markdown
  wget2 "$url" -O - -q | pandoc -f html -t gfm -o "output_md/${filename}.md"

done <api-url.txt

echo "Done! Check the 'output_md' folder."
