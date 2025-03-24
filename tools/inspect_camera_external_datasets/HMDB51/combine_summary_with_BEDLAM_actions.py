import os
import pandas as pd
import re
from collections import defaultdict

# Input and output file paths
SUMMARY_FILE = "camera_angle_summary.xlsx"  # Input file
OUTPUT_FILE = "camera_angle_grouped.xlsx"  # Output file

# Define the similar action groups
action_groups = {
    "bend": ["pick", "situp"],
    # "dance": ["flic_flac"],
    "kick": ["kick", "kick_ball"],
    # "kneel": ["draw_sword"],
    # "perform": ["flic_flac", "fencing", "sword", "sword_exercise"],
    "run": ["run"],
    # "squat": ["situp", "pick"],
    "stretch": ["handstand", "somersault"],
    "take_pick_something_up": ["pick", "pour"],
    "turn": ["turn", "somersault"],
    "walk": ["walk", "climb_stairs"],
    # "yoga": []
}

# Load the summary file
if not os.path.exists(SUMMARY_FILE):
    print(f"Error: File {SUMMARY_FILE} not found!")
    exit()

df_summary = pd.read_excel(SUMMARY_FILE)


# Function to parse and aggregate camera angles
def aggregate_camera_angles(angle_list):
    """Aggregates camera angles by summing their counts."""
    angle_counts = defaultdict(int)

    for angles in angle_list:
        if pd.isna(angles):
            continue
        for match in re.findall(r"([\w\s()-]+)\s\((\d+)\)", angles):
            angle_name, count = match[0].strip(), int(match[1])
            angle_counts[angle_name] += count

    return ", ".join(
        [f"{angle} ({count})" for angle, count in sorted(angle_counts.items())]) if angle_counts else "No Data"


# Create a dictionary to store aggregated camera angles per action category
camera_angle_dict = {}

for category, actions in action_groups.items():
    # Extract camera angles for all matching actions
    relevant_angles = df_summary[df_summary["Action"].isin(actions)]["Most Frequent Camera Angles"].tolist()
    # Aggregate camera angles properly
    camera_angle_dict[category] = aggregate_camera_angles(relevant_angles)

# Convert the dictionary to a DataFrame
df_camera_angles = pd.DataFrame(list(camera_angle_dict.items()), columns=["Action Category", "Camera Angles"])

# Delete previous Excel file if it exists
if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)
    print(f"Deleted existing file: {OUTPUT_FILE}")

# Save the grouped data to an Excel file
df_camera_angles.to_excel(OUTPUT_FILE, index=False)
print(f"Grouped camera angles saved to {OUTPUT_FILE}")
