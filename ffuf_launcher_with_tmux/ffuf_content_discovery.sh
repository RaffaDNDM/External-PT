#!/bin/bash

# Function to display usage instructions
usage() {
    echo "Usage: $0 -u <url_file> -w <wordlist> [-t <threads>] [-d <dir>]"
    echo "  -u <url_file>   : Path to the file containing the list of URLs"
    echo "  -w <wordlist>   : Path to the wordlist file for fuzzing"
    echo "  -t <threads>    : Optional number of threads (default is 50)"
    echo "  -r <rate>       : Maximum requests rate"
    exit 1
}

THREADS=5
RATE=30

# Parse command-line arguments
while getopts "u:w:t:r:" opt; do
    case "$opt" in
        u) URL_FILE="$OPTARG" ;;    # URL list file
        w) WORDLIST="$OPTARG" ;;    # Wordlist file
        t) THREADS="$OPTARG" ;;     # Threads (optional, defaults to 5)
        r) RATE="$OPTARG" ;;        # Rate (optional, defaults to 30)
        *) usage ;;                 # Invalid option, show usage
    esac
done

# Check if the required arguments are provided
if [ -z "$URL_FILE" ] || [ -z "$WORDLIST" ]; then
    echo "Error: Missing required arguments"
    usage
fi

# Check if the URL file exists
if [ ! -f "$URL_FILE" ]; then
    echo "Error: URL file '$URL_FILE' does not exist."
    exit 2
fi

# Check if the wordlist file exists
if [ ! -f "$WORDLIST" ]; then
    echo "Error: Wordlist file '$WORDLIST' does not exist."
    exit 3
fi

# Wordlist for fuzzing (you can change this)
WORDLIST_NAME=$(basename "$WORDLIST")  # Extract the filename
LAST_WORD=$(echo "$WORDLIST_NAME" | sed 's/.*\-\([a-zA-Z0-9]*\)\.txt/\1/')  # Extract the last word from the filename

# Check if the folder does not exist
if [ ! -d "./results" ]; then
    # Create the folder
    mkdir -p "./results"
    echo "Folder created: ./results"
else
    echo "Folder already exists: ./results"
fi

# Loop through each URL in the list
while IFS= read -r url; do
    echo "Fuzzing $url"
    ffuf -u "$url/FUZZ" -ac -w "$WORDLIST" -t "$THREADS" -rate "$RATE" -o "./results/${url//[:\/.]/_}_${LAST_WORD}.csv" -of csv -r -v

done < "$URL_FILE"
