import json
import csv

input_json_file = "C:/Users/edwar/SocialPositivityData/YelpData/yelp_academic_dataset_review.json/yelp_academic_dataset_review.json"
output_csv_file = "C:/Users/edwar/SocialPositivityData/YelpData/yelp.csv"

with open(input_json_file, 'r', encoding='utf-8') as json_file:
    data = [json.loads(line) for line in json_file]

fieldnames = [key for key in data[0].keys() if key != ("text" or "title" or "images")]

with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    writer.writeheader()
    
    i = 0
    for row in data:
        i+=1
        row_without_review_text = {key: row[key] for key in fieldnames}
        writer.writerow(row_without_review_text)
        if(i == 10000000):
            break

print(f"CSV file '{output_csv_file}' has been created successfully.")