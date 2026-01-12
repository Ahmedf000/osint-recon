#!/bin/bash

TARGET="example.com"
OUTPUT_DIR="scan_results_$(date +%Y%m%d)"

mkdir -p $OUTPUT_DIR

echo "Starting comprehensive scan of $TARGET..."

python osint.py -t $TARGET -d 1 -o "$OUTPUT_DIR/pdfs.json"
python osint.py -t $TARGET -d 5 -o "$OUTPUT_DIR/env_files.json"
python osint.py -t $TARGET -d 9 -o "$OUTPUT_DIR/sql_dumps.json"

python osint.py -t $TARGET -d 11 -o "$OUTPUT_DIR/login_pages.json"
python osint.py -t $TARGET -d 12 -o "$OUTPUT_DIR/admin_panels.json"

python osint.py -t $TARGET -d 23 -o "$OUTPUT_DIR/subdomains.json"

python osint.py -t $TARGET -d 15 -o "$OUTPUT_DIR/api_endpoints.json"

echo "Scan complete! Results in $OUTPUT_DIR/"