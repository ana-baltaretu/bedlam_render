import csv
import json

# Input and output file names
input_csv_filename = "bend_input.csv"  # Replace with the actual CSV file name
output_json_filename = "whitelist_bend_animations.json"
output_csv_path = "bend_gender.csv"

# Dictionary to store the processed animation_data
animation_data = {}
gender_data = [["Name", "Gender"]]

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

            gender = 'm' if body_type.startswith("male") else 'f' if body_type.startswith("female") else ''
            if gender:  # Only add if a valid gender is found
                gender_data.append([body_type, gender])

# Save to JSON file
with open(output_json_filename, "w", encoding="utf-8") as json_file:
    json.dump(animation_data, json_file, indent=4)

# Write the extracted gender data to a new CSV file
with open(output_csv_path, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(gender_data)

print(f"Converted data saved to {output_json_filename}")
