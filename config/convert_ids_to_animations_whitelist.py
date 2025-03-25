import csv
import json
import os

clothing_folder_path = r"C:\bedlam\material_4rendering\batch_01\clothing_abc"

# Input and output file names
animation_name = "cartwheel"
input_csv_filename = f"./{animation_name}/{animation_name}_animation_ids.csv"
output_json_filename = f"./{animation_name}/whitelist_{animation_name}_animations.json"

# Dictionary to store the processed animation_data
animation_data = {}

# Read the CSV file
with open(input_csv_filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the first row
    for row in reader:
        if row:  # Ensure the row is not empty
            parts = row[0].rsplit('_', 1)  # Split into prefix and sequence number
            body_type = parts[0]
            animation_id = parts[1]
            if body_type not in animation_data:
                animation_data[body_type] = []
            animation_data[body_type].append(animation_id)

# Prepare the filtered result
filtered_animation_data = {}

for body_type, animation_ids in animation_data.items():
    body_path = os.path.join(clothing_folder_path, body_type, "clothing_simulations")
    if os.path.isdir(body_path):
        available_animations = set(os.listdir(body_path))
        filtered_ids = [aid for aid in animation_ids if aid in available_animations]
        if filtered_ids:
            filtered_animation_data[body_type] = filtered_ids

print(len(filtered_animation_data))
print(filtered_animation_data)

# Save the filtered animation data
with open(output_json_filename, "w", encoding="utf-8") as json_file:
    json.dump(filtered_animation_data, json_file, indent=4)

print(f"Filtered data saved to {output_json_filename}")
