import re
import csv
import chardet

# File paths
input_file = 'movies.dat'
output_file = 'movies_dat.csv'

# Regular expression to extract title and release year
title_year_regex = re.compile(r"^(.*) \((\d{4})\)$")

# Step 1: Detect the encoding of the input file
with open(input_file, 'rb') as file:
    raw_data = file.read(10000)  # Read a sample of the file (e.g., 10 KB)
    result = chardet.detect(raw_data)
    detected_encoding = result['encoding']
    print(f"Detected Encoding: {detected_encoding} (Confidence: {result['confidence']})")

# Step 2: Process the file with the detected encoding
try:
    with open(input_file, 'r', encoding=detected_encoding) as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        # CSV writer setup
        writer = csv.writer(outfile)
        # Write header to the CSV
        writer.writerow(['movie_id', 'movie_title', 'release_year', 'genres'])
        
        # Process each line in the input file
        for line in infile:
            # Split line by '::'
            parts = line.strip().split('::')
            if len(parts) != 3:
                continue  # Skip malformed lines
            
            movie_id, raw_title, genres = parts
            # Match the title and year using regex
            match = title_year_regex.match(raw_title)
            if match:
                movie_title, release_year = match.groups()
                # Write the processed row to the CSV
                writer.writerow([movie_id, movie_title, release_year, genres])
            else:
                print(f"Skipping line due to unmatched title/year format: {line.strip()}")
except UnicodeDecodeError as e:
    print(f"Encoding issue: {e}")
