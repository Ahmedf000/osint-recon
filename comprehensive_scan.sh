#!/bin/bash

TARGET="example.com"
OUTPUT_DIR="scan_results_$(date +%Y%m%d)"

mkdir -p $OUTPUT_DIR

echo "Starting comprehensive scan of $TARGET..."

python3 osint.py -t $TARGET -d 1 -o "$OUTPUT_DIR/pdfs.json"
python3 osint.py -t $TARGET -d 5 -o "$OUTPUT_DIR/env_files.json"
python3 osint.py -t $TARGET -d 9 -o "$OUTPUT_DIR/sql_dumps.json"

python3 osint.py -t $TARGET -d 11 -o "$OUTPUT_DIR/login_pages.json"
python3 osint.py -t $TARGET -d 12 -o "$OUTPUT_DIR/admin_panels.json"

python3 osint.py -t $TARGET -d 23 -o "$OUTPUT_DIR/subdomains.json"

python3 osint.py -t $TARGET -d 15 -o "$OUTPUT_DIR/api_endpoints.json"

echo "Scan complete! Results in $OUTPUT_DIR/"
