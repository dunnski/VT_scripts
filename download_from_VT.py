import os
import csv
import requests
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import argparse

def load_api_keys():
    load_dotenv()

# Load API keys from .env file
load_api_keys()

# You must replace edit your '.env' file with your actual API key from VirusTotal.
API_KEY = os.getenv("vti_api_key")
API_URL = 'https://www.virustotal.com/api/v3/files/{}'

# Parse command line arguments
parser = argparse.ArgumentParser(
    description='Download files from VirusTotal based on a CSV of hashes or a single hash.',
    epilog="""
    Examples of usage:

    To download files using a CSV of hashes:
      python download_from_VT.py folder_name --csv_file_name hashes.csv

    To download a single file using a hash:
      python download_from_VT.py  folder_name --single_hash <hash_value>
      
    """
)
parser.add_argument('dest_folder_name', help='Name of folder to write to')
parser.add_argument('--csv_file_name', help='CSV file you want to use')
parser.add_argument('--single_hash', help='Single hash you want to download')
args = parser.parse_args()

# Get the home directory of the current user
home_directory = os.path.expanduser('~')

# Construct the path to the desktop
desktop_path = os.path.join(home_directory, 'Desktop')

# Use the provided arguments for destination folder and CSV file
dest_path = os.path.join(home_directory, args.dest_folder_name)
if args.csv_file_name:
    CSV_FILE_PATH = os.path.join(desktop_path, args.csv_file_name)

# Function to download a file from VirusTotal
def download_file_from_virustotal(malware_name, file_hash):
    # Create the folder if it doesn't exist
    folder_path = os.path.join(dest_path, malware_name)
    os.makedirs(folder_path, exist_ok=True)
    
    # VirusTotal API endpoint for file download
    download_url = f'https://www.virustotal.com/api/v3/files/{file_hash}/download'
    headers = {'x-apikey': API_KEY}
    
    # Make the request to download the file
    response = requests.get(download_url, headers=headers)
    
    if response.status_code == 200:
        file_path = os.path.join(folder_path, file_hash)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"File {file_hash} downloaded to {folder_path}")
    else:
        print(f"Failed to download file {file_hash}. Status code: {response.status_code} - {response.text}")

# Function to read the CSV and initiate the download process
def process_csv_and_download_files(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        
        # Use ThreadPoolExecutor to parallelize downloads
        with ThreadPoolExecutor(max_workers=5) as executor:
            for row in reader:
                malware_name, file_hash = row[0], row[1]
                # Submit the task to the executor
                executor.submit(download_file_from_virustotal, malware_name, file_hash)

# Run the script
if __name__ == "__main__":
    if args.csv_file_name:
        process_csv_and_download_files(CSV_FILE_PATH)
    elif args.single_hash:
        download_file_from_virustotal('single_hash', args.single_hash)
    else:
        print("Please provide either a CSV file or a single hash.")
