#!/usr/bin/env bash

result_dir="$1"
script_dir="$(dirname "$0")"
# Get git root directory
root_dir="$(git rev-parse --show-toplevel)"

# Change to root directory to ensure relative paths work
cd "$root_dir"

# Check if log_files.txt exists before trying to read it
if [ -f "${result_dir}/log_files.txt" ]; then
    # Copy logs from the project root
    while read logfile; do
        cp "$logfile" "$result_dir"
      done < "${result_dir}/log_files.txt"
else
    echo "Warning: ${result_dir}/log_files.txt not found, skipping log file copying"
fi

# Create the archive alongside the folder
tar -czf "${result_dir}.tar.gz" -C "$(dirname "$result_dir")" "$(basename "$result_dir")"
