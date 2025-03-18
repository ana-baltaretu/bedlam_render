import os
import numpy as np
import csv


def find_npz_files(folder_path):
    """Recursively finds all .npz files in the given folder and its subfolders."""
    npz_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.npz'):
                npz_files.append(os.path.join(root, file).replace('\\', '/'))
    return npz_files


def extract_motion_label(file_path):
    """Extracts the motion label from the motion_info variable in an .npz file."""
    try:
        with np.load(file_path) as data:
            if 'motion_info' in data:
                motion_info = data['motion_info']
                if len(motion_info) > 0:
                    return motion_info[0].lower()  # First element is the motion label, converted to lowercase because "March" was uppercase for some reason
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
    return "unknown"    # Ideally you would never get here


def group_by_body_type(folder_path):
    """Groups npz files by body type (direct children of the given folder)."""
    groups = {}

    for body_type in os.listdir(folder_path):
        body_type_path = os.path.join(folder_path, body_type).replace('\\', '/')
        if os.path.isdir(body_type_path):
            npz_files = find_npz_files(body_type_path)
            if npz_files:
                groups[body_type] = [(file_path, extract_motion_label(file_path), generate_id(body_type, file_path)) for
                                     file_path in npz_files]

    return groups


def generate_id(body_type, file_path):
    """Generates an ID combining body type and animation number."""
    try:
        file_path = file_path.replace('\\', '/')
        parts = file_path.split('/')

        if len(parts) > 4:
            anim_number = parts[-2]  # Extract animation number
        else: anim_number = "unknown"

        return f"{body_type}_{anim_number}"
    except Exception as e:
        print(f"Error generating ID for {file_path}: {e}")
        return "unknown"


def save_to_csv(groups, output_file):
    """Saves the grouped npz file data to a CSV file."""
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Unreal animation ID", "Body Type", "Motion Label", "File Path"])

        for body_type, files in groups.items():
            for file_path, motion_label, file_id in files:
                writer.writerow([file_id, body_type, motion_label, file_path])


def main():
    # Input your file path when prompted, for me: "C:/bedlam/animations/gendered_ground_truth"
    parent_folder = input("\nEnter folder path to top of .npz files: ").strip()

    if not os.path.isdir(parent_folder):
        print("Invalid folder path.")
        return

    groups = group_by_body_type(parent_folder)
    output_file = "motion_labels.csv"
    save_to_csv(groups, output_file)
    print(f"Motion labels saved to {output_file}")


if __name__ == "__main__":
    main()