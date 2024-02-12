import os
from pathlib import Path
import pefile
import datetime

# Get the home directory of the current user
home_directory = os.path.expanduser('~')
# Construct the path to the desktop
desktop_path = os.path.join(home_directory, 'Desktop')
# ***Make sure you change the name of the destination folder you want to store files in***
parent_folder_path = os.path.join(home_directory, 'Desktop/Crowdstrike_Efficacy_Test/')

def modify_pe_timestamp(file_path, output_file):
    try:
        pe = pefile.PE(file_path)
        # PE timestamps are in Unix epoch format. Calculate the timestamp for one day before the current date.
        new_timestamp = int((datetime.datetime.now() - datetime.timedelta(days=1)).timestamp())
        pe.FILE_HEADER.TimeDateStamp = new_timestamp
        
        # Save the modified PE file
        pe.write(filename=output_file)

        print(f"Successfully modified the timestamp of {file_path}. Output file: {output_file}")
    except Exception as e:
        print(f"Error modifying {file_path}: {e}")

def process_folder(target_folder):
    # Ensure the target folder is a Path object for easier path manipulations
    target_folder = Path(target_folder)
    modded_folder = target_folder / "modded"

    # Create the modded directory if it does not exist
    if not modded_folder.exists():
        modded_folder.mkdir()

    # Iterate over every .exe and .dll file in the target folder
    for file in target_folder.iterdir():
        if file.is_file() and file.suffix in ['.exe', '.dll']:  # Filter for PE files
            # Construct the output file path
            output_file = modded_folder / f"{file.stem}_time_stamp_modded{file.suffix}"
            modify_pe_timestamp(file, output_file)
        else:
            print(f"{file} is not a PE file.")

# Example usage
target_folder = os.path.join(parent_folder_path, 'Windows/Cobalt Strike')  # Replace with the path to your target folder

process_folder(target_folder)