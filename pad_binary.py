import os
from pathlib import Path

# Get the home directory of the current user
home_directory = os.path.expanduser('~')
# Construct the path to the desktop
desktop_path = os.path.join(home_directory, 'Desktop')
# ***Make sure you change the name of the destination folder you want to store files in***
parent_folder_path = os.path.join(home_directory, 'Desktop/MRO_testing/Windows')

def append_nops_to_executable(file_path, num_nops, output_file):
    nop = b'\x90'  # NOP opcode in x86 assembly
    try:
        with open(file_path, 'rb') as original_file:
            data = original_file.read()
            data += nop * num_nops  # Append the specified number of NOPs

        with open(output_file, 'wb') as modified_file:
            modified_file.write(data)

        print(f"Successfully appended {num_nops} NOPs to {file_path}. Output file: {output_file}")
    except IOError as e:
        print(f"Error: {e}")

def process_folder(target_folder, num_nops):
    # Ensure the target folder is a Path object for easier path manipulations
    target_folder = Path(target_folder)
    modded_folder = target_folder / "modded"

    # Create the modded directory if it does not exist
    if not modded_folder.exists():
        modded_folder.mkdir()

    # Iterate over every file in the target folder
    for file in target_folder.iterdir():
        if file.is_file():  # Make sure to skip directories
            # Construct the output file path
            output_file = modded_folder / f"{file.stem}_modded{file.suffix}"
            append_nops_to_executable(file, num_nops, output_file)

# Example usage
target_folder = os.path.join(parent_folder_path, 'NanoCore')  # Replace with the path to your target folder
num_nops = 10  # Number of NOP bytes to append

process_folder(target_folder, num_nops)
