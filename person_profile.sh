#!/bin/bash

NAME="$1"
OUTPUT_DIR="profile_$(echo $NAME | tr ' ' '_')_$(date +%Y%m%d)"

mkdir -p $OUTPUT_DIR

echo "Creating profile for: $NAME"

python3 osint.py -t "$NAME" -d 63 -o "$OUTPUT_DIR/linkedin.json"
python3 osint.py -t "$NAME" -d 67 -o "$OUTPUT_DIR/github.json"
python3 osint.py -t "$NAME" -d 90 -o "$OUTPUT_DIR/work_history.json"

python3 osint.py -t "$NAME" -d 51 -o "$OUTPUT_DIR/resume.json"
python3 osint.py -t "$NAME" -d 56 -o "$OUTPUT_DIR/papers.json"

python3 osint.py -t "$NAME" -d 75 -o "$OUTPUT_DIR/email.json"

python3 osint.py -t "$NAME" -d 64 -o "$OUTPUT_DIR/twitter.json"
python3 osint.py -t "$NAME" -d 65 -o "$OUTPUT_DIR/facebook.json"

echo "Profile complete! Results in $OUTPUT_DIR/"
