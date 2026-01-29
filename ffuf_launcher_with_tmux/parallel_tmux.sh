#!/bin/bash

# Define the list of target files
target_directory="${1:-targets}"

# Define the command you want to run in each tmux session
ffuf_files_command="./ffuf_content_discovery.sh -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt -t 5 -r 30"
ffuf_dir_command="./ffuf_content_discovery.sh -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -t 5 -r 30"

# Create a new tmux session for each target in the list
for target_file in "$target_directory"/*.txt; do
    # Skip if no .txt files are found
    if [[ ! -f "$target_file" ]]; then
        echo "No .txt files found in $target_directory"
        exit 1
    fi

    session_files_name="files_$(basename "$target_file" .txt)"
    echo $session_files_name
    session_dir_name="dir_$(basename "$target_file" .txt)"
    echo $session_dir_name

    echo "tmux new-session -d -s" "$session_files_name" "$ffuf_files_command -u $target_file"
    echo "Started tmux session: $session_files_name with target: $target_file"
    tmux new-session -d -s "$session_files_name" "$ffuf_files_command -u $target_file"

    echo "tmux new-session -d -s" "$session_dir_name" "$ffuf_dir_command -u $target_file"
    echo "Started tmux session: $session_dir_name with target: $target_file"
    tmux new-session -d -s "$session_dir_name" "$ffuf_dir_command -u $target_file"

done

echo "All tmux sessions started!"
