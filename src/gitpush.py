import os
import time
import subprocess
from datetime import datetime
import hashlib

def hash_file(filename):
    """Generate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        while chunk := f.read(4096):  # Read in chunks for efficiency
            sha256.update(chunk)
    file_hash = sha256.hexdigest()
    return file_hash

def backup_and_push_to_git(zip_fn, branch='backup'):
    """
    Hash a file, check for changes, and push to git repository.
    
    zip_fn: Path to the zip file (default: 'compressed/UoE_00.zip')
    branch: Name of the git branch to use (default: 'backup')
    """
    start_time = time.time()

    try:
        subprocess.run(["git", "checkout", branch], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["git", "checkout", "-b", branch], check=True)

    # Get the current hash of the file
    file_hash = hash_file(zip_fn)
    print(f"SHA-256 Hash: {file_hash}")

    # Define file paths
    txt_fn = zip_fn.replace('.zip', '.txt')

    # Write the hash to the text file
    with open(txt_fn, 'w') as f:
        f.write(file_hash)

    # Check if the txt file exists to compare the old hash
    if os.path.exists(txt_fn):
        with open(txt_fn, 'r') as f:
            old_hash = f.read().strip()
        
        # Compare the old and new hashes
        if old_hash == file_hash:
            print("No change in the file. Same hash.")
            commit_msg = f"No changes detected. Same hash: {file_hash}"
            subprocess.run(["git", "add", txt_fn], check=True)
            subprocess.run(["git", "add", "compress_sync.py"], check=True)
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "--set-upstream", "origin", branch], check=True)
        else:
            print("File has changed. New hash generated.")
            commit_msg = f"File change detected. New hash: {file_hash}"
            subprocess.run(["git", "add", zip_fn, txt_fn, "compress_sync.py"], check=True)
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "--set-upstream", "origin", branch], check=True)
    else:
        print(f"Text file {txt_fn} does not exist. Creating a new one with the hash.")
        with open(txt_fn, 'w') as f:
            f.write(file_hash)
        commit_msg = f"Initial backup: {file_hash}"
        subprocess.run(["git", "add", zip_fn, txt_fn, "compress_sync.py"], check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "--set-upstream", "origin", branch], check=True)

    elapsed_time = time.time() - start_time
    print(f"Git push completed in {elapsed_time:.2f} seconds")
