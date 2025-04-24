import json
import csv

# Input JSON file path
input_json_file = 'C:/Users/edwar/Downloads/goodreads_reviews_fantasy_paranormal.json/goodreads_reviews_fantasy_paranormal.json'
# Output CSV file path
output_csv_file = 'C:/Users/edwar/SocialPositivityData/GoodreadsData/goodreads_fantasy.csv'

with open(input_json_file, 'r', encoding='utf-8') as json_file:
    # Read all lines and parse each line as a JSON object
    data = [json.loads(line) for line in json_file]

# Define the CSV column headers, excluding "review_text"
fieldnames = [key for key in data[0].keys() if key != "review_text"]

# Write the data to a CSV file
with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write each row of data, excluding "review_text"
    for row in data:
        # Create a new dictionary without the "review_text" field
        row_without_review_text = {key: row[key] for key in fieldnames}
        writer.writerow(row_without_review_text)

print(f"CSV file '{output_csv_file}' has been created successfully.")