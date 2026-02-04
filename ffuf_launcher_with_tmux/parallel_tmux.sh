#!/bin/bash

MODE="$1"
target_directory="${2:-targets}"

ffuf_files_command="./ffuf_content_discovery.sh -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt -t 5 -r 30"
ffuf_dir_command="./ffuf_content_discovery.sh -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -t 5 -r 30"

case "$MODE" in
  start)
    for target_file in "$target_directory"/*.txt; do
      if [[ ! -f "$target_file" ]]; then
        echo "No .txt files found in $target_directory"
        exit 1
      fi

      session_files_name="files_$(basename "$target_file" .txt)"
      session_dir_name="dir_$(basename "$target_file" .txt)"

      echo "Starting tmux session: $session_files_name"
      tmux new-session -d -s "$session_files_name" \
        "$ffuf_files_command -u $target_file"

      echo "Starting tmux session: $session_dir_name"
      tmux new-session -d -s "$session_dir_name" \
        "$ffuf_dir_command -u $target_file"
    done

    echo "All tmux sessions started!"
    ;;

  pause|restart)
    echo "Sending carriage return to ffuf tmux sessions..."

    tmux list-sessions -F '#S' | while read session; do
      if [[ "$session" == files_* || "$session" == dir_* ]]; then
        echo "Sending Enter to $session"
        tmux send-keys -t "$session" C-m
      fi
    done

    echo "Done."
    ;;

  kill)
    echo "Killing ffuf tmux sessions..."

    tmux list-sessions -F '#S' | while read session; do
      if [[ "$session" == files_* || "$session" == dir_* ]]; then
        echo "Killing session: $session"
        tmux kill-session -t "$session"
      fi
    done

    echo "All ffuf tmux sessions killed."
    ;;

  *)
    echo "Usage:"
    echo "  $0 start [target_directory]"
    echo "  $0 pause"
    echo "  $0 restart"
    echo "  $0 kill"
    exit 1
    ;;
esac
