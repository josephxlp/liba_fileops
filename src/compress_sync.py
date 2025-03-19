import os
import time
import tarfile
import zipfile
import subprocess
from datetime import datetime

def compress_folder(folder_path, output_folder="compressed", compression_type="tar"):
    print("compress_folder started")
    """
    Compresses a folder into a zip or tar.gz archive with a timestamp.

    Parameters:
        folder_path (str): Path to the folder to be compressed.
        output_folder (str): Path where the compressed file should be stored.
        compression_type (str): Compression type ("zip" or "tar"). Default is "tar".

    Returns:
        str: Path to the created compressed file.
    """
    start_time = time.time()

    if not os.path.isdir(folder_path):
        raise ValueError(f"Invalid directory: {folder_path}")

    folder_name = os.path.basename(os.path.normpath(folder_path))
    timestamp = datetime.now().strftime("%Y%m%d__%H%M%S")  # Unique timestamp
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, f"{folder_name}_{timestamp}")

    if compression_type == "zip":
        output_file += ".zip"
        with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)
    elif compression_type == "tar":
        output_file += ".tar.gz"
        with tarfile.open(output_file, "w:gz") as tarf:
            tarf.add(folder_path, arcname=folder_name)
    else:
        raise ValueError("Invalid compression type. Choose 'zip' or 'tar'.")

    elapsed_time = time.time() - start_time
    print(f"Compression completed in {elapsed_time:.2f} seconds")
    print("compress_folder completed")

    return output_file

def remove_large_files(threshold_mb=100):
    print("remove_large_files started")
    """
    Removes files larger than the specified threshold to prevent Git push failures.

    Parameters:
        threshold_mb (int): File size limit in MB (default is 100MB).
    """
    for root, _, files in os.walk("."):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.isfile(file_path):
                    size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    if size_mb > threshold_mb:
                        print(f"Removing large file: {file_path} ({size_mb:.2f}MB)")
                        #os.remove(file_path)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    print("remove_large_files completed")

def sync_with_dvc(remote_name="onedrive"):
    print("sync_with_dvc started")
    """
    Sync the compressed files with DVC and push to remote storage.

    Parameters:
        remote_name (str): Name of the DVC remote (e.g., "onedrive", "google-drive").
    """
    start_time = time.time()

    try:
        subprocess.run(["dvc", "add", "data/compressed/"], check=True)
        subprocess.run(["dvc", "push", "-r", remote_name], check=True)
        print(f"Synced with DVC remote '{remote_name}'")
    except subprocess.CalledProcessError as e:
        print(f"DVC sync failed: {e}")

    elapsed_time = time.time() - start_time
    print(f"DVC sync completed in {elapsed_time:.2f} seconds")
    print("sync_with_dvc completed")

if __name__ == "__main__":
    from upaths import form_codebase_dpath
    from gitpush import backup_and_push_to_git

    output_folder = "data/compressed"
    os.makedirs(output_folder, exist_ok=True)

    compressed_file = compress_folder(form_codebase_dpath, output_folder, compression_type="zip")
    print(f"Compressed file: {compressed_file}")

    # Send notification on successful compression
    os.system(f'notify-send "Backup Process" "Backup completed: {compressed_file}"')

    # Push backup to Git
    backup_and_push_to_git(zip_fn=compressed_file, branch="backup")

    # Uncomment to enable DVC syncing
    # sync_with_dvc("onedrive")
    # sync_with_dvc("google-drive")
