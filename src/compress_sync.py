import os
import shutil
import time
import subprocess
from datetime import datetime

def compress_folder(folder_path, output_folder="compressed", compression_type='zip'):
    print('compress_folder started')
    """
    Compresses a folder into a zip or tar archive with a timestamp.

    Parameters:
        folder_path (str): Path to the folder to be compressed.
        output_folder (str): Path where the compressed file should be stored.
        compression_type (str): Compression type ('zip' or 'tar'). Default is 'zip'.

    Returns:
        str: Path to the created compressed file.
    """
    start_time = time.time()

    if not os.path.isdir(folder_path):
        raise ValueError(f"Invalid directory: {folder_path}")

    folder_name = os.path.basename(os.path.normpath(folder_path))
    timestamp = datetime.now().strftime("%Y%m%d__%H%M%S")
    timestamp = '00'
    os.makedirs(output_folder, exist_ok=True)

    if compression_type == 'zip':
        output_file = os.path.join(output_folder, f"{folder_name}_{timestamp}.zip")
        shutil.make_archive(output_file[:-4], 'zip', folder_path)
    elif compression_type == 'tar':
        output_file = os.path.join(output_folder, f"{folder_name}_{timestamp}.tar.gz")
        shutil.make_archive(output_file[:-7], 'gztar', folder_path)
    else:
        raise ValueError("Invalid compression type. Choose 'zip' or 'tar'.")

    elapsed_time = time.time() - start_time
    print(f"Compression completed in {elapsed_time:.2f} seconds")
    print('compress_folder completed')

    return output_file

def remove_large_files(threshold_mb=100):
    print('remove_large_files started')
    """
    Removes files larger than the specified threshold to prevent Git push failures.

    Parameters:
        threshold_mb (int): File size limit in MB (default is 100MB).
    """
    for root, _, files in os.walk("."):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                if size_mb > threshold_mb:
                    print(f"Removing large file: {file_path} ({size_mb:.2f}MB)")
                    #os.remove(file_path)

    print('remove_large_files completed')

def sync_with_dvc(remote_name="onedrive"):
    print('sync_with_dvc started')
    """
    Sync the compressed files with DVC and push to remote storage.

    Parameters:
        remote_name (str): Name of the DVC remote (e.g., 'onedrive', 'google-drive').
    """
    start_time = time.time()

    try:
        subprocess.run(["dvc", "add", "compressed/"], check=True)
        subprocess.run(["dvc", "push", "-r", remote_name], check=True)
        print(f"Synced with DVC remote '{remote_name}'")
    except subprocess.CalledProcessError as e:
        print(f"DVC sync failed: {e}")

    elapsed_time = time.time() - start_time
    print(f"DVC sync completed in {elapsed_time:.2f} seconds")
    print('sync_with_dvc completed')

if __name__ == "__main__":
    from upaths import form_codebase_dpath
    from gitpush import backup_and_push_to_git

    output_folder = "data/compressed"
    os.makedirs(output_folder, exist_ok=True)

    compressed_file = compress_folder(form_codebase_dpath, output_folder, compression_type='zip')
    print(f"Compressed file: {compressed_file}")

    os.system(f'notify-send "Backup Process" "Backup completed successfully: {compressed_file}"')
    backup_and_push_to_git(zip_fn=compressed_file, branch="backup")

    #push_to_git()
    #sync_with_dvc("onedrive")
    #sync_with_dvc("google-drive")
    # add another script that runs this on schedule and sends a notification
    # compress to the based into the data folder , and use dvc there 
