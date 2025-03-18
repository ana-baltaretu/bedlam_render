import os
import numpy as np


def find_npz_files(folder_path):
    """Recursively finds all .npz files in the given folder and its subfolders."""
    npz_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.npz'):
                npz_files.append(os.path.join(root, file))
    return npz_files


def inspect_npz(file_path):
    """Loads and displays the contents of an .npz file."""
    try:
        with np.load(file_path) as data:
            print(f"\nContents of {file_path}:")
            for key in data.files:
                print(f" - {key}: shape {data[key].shape}, dtype {data[key].dtype}")

            while True:
                var_choice = input("\nEnter a variable name to view its contents (or 'q' to return): ").strip()
                if var_choice.lower() == 'q':
                    break
                if var_choice in data.files:
                    print(f"\nContents of {var_choice}:\n", data[var_choice])
                else:
                    print("Invalid variable name. Please choose from the listed variables.")
    except Exception as e:
        print(f"Error loading {file_path}: {e}")


def main():
    folder_path = "C:/bedlam/animations/gendered_ground_truth/female_25_it_4002"

    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return

    npz_files = find_npz_files(folder_path)

    if not npz_files:
        print("No .npz files found in the folder or its subfolders.")
        return

    print("\nAvailable .npz files:")
    for i, file in enumerate(npz_files):
        print(f"{i + 1}. {file}")

    while True:
        choice = input("\nEnter the number of a file to inspect (or 'q' to quit): ").strip()

        if choice.lower() == 'q':
            break

        if not choice.isdigit() or int(choice) not in range(1, len(npz_files) + 1):
            print("Invalid choice. Please enter a valid number.")
            continue

        file_path = npz_files[int(choice) - 1]
        inspect_npz(file_path)


if __name__ == "__main__":
    main()
