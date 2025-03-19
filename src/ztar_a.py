from fileops import create_tarball
from concurrent.futures import ProcessPoolExecutor
import os

def send_notification(message, duration=300000):
    """
    Sends a desktop notification using notify-send (Linux).

    Args:
        message (str): Notification message.
        duration (int): Duration in milliseconds (default: 5 minutes).
    
    Returns:
        None
    """
    try:
        os.system(f'notify-send -t {duration} "Trash Cleanup" "{message}"')
    except Exception as e:
        print(f"Failed to send notification: {e}")

# Define source and destination directories
# source_dir = "/media/ljp238/12TBWolf/ARCHIEVE/PBAND_DTM/"
# destination_dir = "/media/ljp238/12TBWolf/ARCHIEVE/TEMP/PBAND/"

source_dir = "/media/ljp238/12TBWolf/ARCHIEVE/LIDAR_DTM/"
destination_dir = "/media/ljp238/12TBWolf/ARCHIEVE/TEMP/LIDAR_DTM/"

if __name__ == "__main__":
    os.makedirs(destination_dir, exist_ok=True)

    tile_names = os.listdir(source_dir)
    if not tile_names:
        print("No files found in source directory.")
    else:
        with ProcessPoolExecutor(max_workers=20) as executor:
            futures = []
            for tile_name in tile_names:
                source_path = os.path.join(source_dir, tile_name)
                destination_path = os.path.join(destination_dir, tile_name + ".tar.gz")

                print(f"Processing: {destination_path}")

                future = executor.submit(create_tarball, source_path, destination_path)
                futures.append(future)

            # Ensure all tasks complete
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing file: {e}")

    print("Done")
    send_notification(message="Tarball creation completed ZTAR_A.py")
