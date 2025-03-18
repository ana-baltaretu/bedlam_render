import os
import requests

# Base URL for HDRI 4K downloads
BASE_URL = "https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/4k/{}_4k.hdr"

# Read whitelist HDRI names from file
WHITELIST_FILE = "../../config/whitelist_hdri.txt"

# Output folder for downloaded HDRIs
OUTPUT_FOLDER = "polyhaven_hdri_downloads"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def download_hdri(name):
    url = BASE_URL.format(name)
    output_path = os.path.join(OUTPUT_FOLDER, f"{name}.hdr")  # Remove _4k from filename

    try:
        print(f"📥 Downloading: {url}")
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(output_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"✅ Successfully downloaded: {output_path}")
        else:
            print(f"❌ Failed to download {name} - HTTP {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error downloading {name}: {e}")

def main():
    with open(WHITELIST_FILE, "r") as file:
        hdri_names = [line.strip() for line in file if line.strip()]

    for name in hdri_names:
        download_hdri(name)

if __name__ == "__main__":
    main()
