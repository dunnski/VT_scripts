import requests
import datetime
import os
from dotenv import load_dotenv
import urllib.parse

def load_api_keys():
    load_dotenv()

# Load API keys from .env file
load_api_keys()

API_KEY = os.getenv("vti_api_key")
HEADERS = {'x-apikey': API_KEY}

def search_and_download(malware_families, file_types):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d_Malwares")
    parent_dir = os.path.join(os.getcwd(), date_str)
    os.makedirs(parent_dir, exist_ok=True)

    download_count = 0  # Counter for tracking the number of downloads

    for family in malware_families:
        if download_count >= 10:
            break  # Stop if we've reached 10 downloads

        # Ensure proper URL encoding for the query
        query = f'{family} and type:{file_types}'
        encoded_query = urllib.parse.quote(query)
        url = f'https://www.virustotal.com/api/v3/intelligence/search?query={encoded_query}'

        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            results = response.json().get('data', [])
            family_dir = os.path.join(parent_dir, family)
            os.makedirs(family_dir, exist_ok=True)

            for result in results:
                if download_count >= 10:
                    break  # Check the counter before each download

                file_id = result['id']
                download_url = f'https://www.virustotal.com/api/v3/files/{file_id}/download'
                download_response = requests.get(download_url, headers=HEADERS, stream=True)

                if download_response.status_code == 200:
                    file_path = os.path.join(family_dir, f"{file_id}.bin")
                    with open(file_path, 'wb') as f:
                        for chunk in download_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Downloaded {file_id} to {file_path}")
                    download_count += 1  # Increment the counter after each download
                else:
                    print(f"Failed to download {file_id}, Status Code: {download_response.status_code}")
        else:
            print(f"Search failed for {family}\nStatus Code: {response.status_code}\n{response.content}")

    print(f"Total downloads: {download_count}")

if __name__ == "__main__":
    malware_families = ['redline']  # Add more as needed
    file_types = 'pe'  # Change to 'macho', 'elf', or other types as required
    search_and_download(malware_families, file_types)
