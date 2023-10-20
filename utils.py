import os
import tempfile
import zipfile
from pathlib import Path


def get_files():
    data_directory = 'data'
    dist_path = os.path.join(os.getcwd(), data_directory)
    if not os.path.exists(dist_path):
        return False

    # List all files in the directory and filter PDF files
    data_files = [filename for filename in os.listdir(data_directory) if filename]
    return data_files


# Helper function to create a zip file containing multiple files
def create_zip_archive(file_paths, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            zipf.write(file_path, arcname=os.path.basename(file_path))
    return zip_filename


def manage_memory(dist_path):
    # Check if the directory exists
    if os.path.exists(dist_path):
        # If it exists, remove all files in the directory
        for filename in os.listdir(dist_path):
            file_path = os.path.join(dist_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        # If the directory doesn't exist, create it
        os.makedirs(dist_path)


def save_json(json_file):
    file_name = "data/data.json"

    if not json_file:
        with open(file_name, "w") as json_file:
            json_file.write("{}")
    else:
        # Open the file in written mode and use json.dump() to write the data to the file
        with open(file_name, "w") as json_output_file:
            json_output_file.write(json_file)