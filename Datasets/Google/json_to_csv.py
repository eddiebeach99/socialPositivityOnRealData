import json
import csv

input_json_file = "C:/Users/edwar/SocialPositivityData/GoogleData/review-Illinois_10.json/review-Illinois_10.json"
output_csv_file = 'C:/Users/edwar/SocialPositivityData/GoogleData/google.csv'

with open(input_json_file, 'r', encoding='utf-8') as json_file:
    data = [json.loads(line) for line in json_file]

fieldnames = [key for key in data[0].keys() if key != ("text" or "title" or "images")]

with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for row in data:
        row_without_review_text = {key: row[key] for key in fieldnames}
        writer.writerow(row_without_review_text)

print(f"CSV file '{output_csv_file}' has been created successfully.")