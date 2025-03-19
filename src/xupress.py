import os
import zipfile
import tarfile
import os
from datetime import datetime

# Function to unzip a .zip file
def unzip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            print(f"Successfully extracted: {zip_path}")
    except Exception as e:
        print(f"Error extracting {zip_path}: {e}")

# Function to extract a .tar or .tar.gz/.tar.bz2 file
def extract_tar_file(tar_path, extract_to):
    try:
        with tarfile.open(tar_path, 'r:*') as tar_ref:
            tar_ref.extractall(extract_to)
            print(f"Successfully extracted: {tar_path}")
    except Exception as e:
        print(f"Error extracting {tar_path}: {e}")

# Function to unzip or extract files in a directory
def extract_files_in_directory(directory, extract_to):
    # Loop through the files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Check if the file is a zip file
        if filename.endswith('.zip'):
            unzip_file(file_path, extract_to)
        
        # Check if the file is a tar file (.tar, .tar.gz, .tar.bz2)
        elif filename.endswith(('.tar', '.tar.gz', '.tar.bz2')):
            extract_tar_file(file_path, extract_to)



def send_notification(message="Script execution completed", duration=5000):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.system(f'notify-send -u normal -t {duration} "{message} at {time_now}"')



if __name__ == '__main__':
    # Set the directory containing the zip and tar files
    # /home/ljp238/Downloads/OneDrive_2025-02-28_RNG.zip
    # name = "TONLESAP"#"MEKONG"#RIONEGRO
    # source_directory = f"/media/ljp238/12TBWolf/ARCHIEVE/RAWROFL/{name}/comprexy"
    # destination_directory = f"/media/ljp238/12TBWolf/ARCHIEVE/RAWROFL/{name}/comprexn"
  
    # name = "S1"# S2
    # source_directory = f"/media/ljp238/12TBWolf/ARCHIEVE/{name}/comprexy"
    # destination_directory = f"/media/ljp238/12TBWolf/ARCHIEVE/{name}/comprexn"
    #source_directory = "/media/ljp238/12TBWolf/ARCHIEVE/EDEMx/TILES/comprexy"
    #destination_directory = "/media/ljp238/12TBWolf/ARCHIEVE/EDEMx/TILES/comprexn"

    #source_directory = "/media/ljp238/12TBWolf/ARCHIEVE/GEDI/GRID/comprexy/"
    #destination_directory = "/media/ljp238/12TBWolf/ARCHIEVE/GEDI/GRID/comprexn/"

    #source_directory = "/media/ljp238/12TBWolf/ARCHIEVE/TRANSACT/7636454/comprexy/"
    #destination_directory = "/media/ljp238/12TBWolf/ARCHIEVE/TRANSACT/7636454/comprexn/"

    source_directory = "/media/ljp238/12TBWolf/ARCHIEVE/EBA3ROIsBrazilianAmazonPointCloudTransact/extra_amazon/comprexy/"
    destination_directory = "/media/ljp238/12TBWolf/ARCHIEVE/EBA3ROIsBrazilianAmazonPointCloudTransact/extra_amazon/comprexn/"

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
        print(f"Created destination directory: {destination_directory}")
    
    # Call function to extract all files in the source directory
    extract_files_in_directory(source_directory, destination_directory)
    print("All files have been extracted.")


send_notification("Processing finished", 100000)  # Display for 7 seconds