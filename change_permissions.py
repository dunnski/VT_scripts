import os
import subprocess

# Get the home directory of the current user
home_directory = os.path.expanduser('~')
# Replace this with the directory you want to process
directory_to_process = os.path.join(home_directory, 'Desktop/Crowdstrike_Efficacy_Test/Linux')

def change_permissions_and_remove_quarantine(directory):
    for root, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Change file permissions with chmod -x
            subprocess.run(['chmod', '777', file_path])
            # Remove the quarantine attribute with xattr -c
            subprocess.run(['xattr', '-c', file_path])
            print(f"Processed file: {file_path}")

# Run the function
change_permissions_and_remove_quarantine(directory_to_process)
