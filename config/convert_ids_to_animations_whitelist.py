import csv
import json

# Input and output file names
animation_name = "run"
input_csv_filename = f"./{animation_name}/{animation_name}_animation_ids.csv"
output_json_filename = f"./{animation_name}/whitelist_{animation_name}_animations.json"

# Dictionary to store the processed animation_data
animation_data = {}

# Read the CSV file
with open(input_csv_filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the first row
    for row in reader:
        print(row)
        if row:  # Ensure the row is not empty
            parts = row[0].rsplit('_', 1)  # Split into prefix and sequence number
            # female_25_us_2681_0014 -> [female_25_us_2681, 0014]

            body_type = parts[0]
            animation_id = parts[1]
            if body_type not in animation_data:
                animation_data[body_type] = []
            animation_data[body_type].append(animation_id)

# Save to JSON file
with open(output_json_filename, "w", encoding="utf-8") as json_file:
    json.dump(animation_data, json_file, indent=4)

print(f"Converted data saved to {output_json_filename}")