from fileops import create_tarball
from concurrent.futures import ProcessPoolExecutor
import os
#from upaths import rsdata_dpath

def send_notification(message):
    """
    Sends a desktop notification using notify-send (Linux).

    Args:
        message (str): Notification message.

    Returns:
        None
    """
    try:
        os.system(f'notify-send "Trash Cleanup" "{message}"')
    except Exception as e:
        print(f"Failed to send notification: {e}")

#data_name = "SENTINEL2"
#data_name = "SENTINEL1"

#from_dpath = f"{rsdata_dpath}/data/{data_name}"
#to_dpath = f"{rsdata_dpath}/compressed/{data_name}"

# from_dpath = "/home/ljp238/Downloads/GEDI_L3_BULK/tiles/"
# to_dpath = "/home/ljp238/Downloads/GEDI_L3_BULK/tiles_compress"

from_dpath = "/home/ljp238/Downloads/GEDI_L3_BULK/data/"
to_dpath = "/home/ljp238/Downloads/GEDI_L3_BULK/data_compress"

from_dpath = "/home/ljp238/Desktop/testing_gedi/POSTPROCESSING_DEMS/"
to_dpath = "/home/ljp238/Desktop/testing_gedi/POSTPROCESSING_DEMS_tiles_ds/"

from_dpath = "/media/ljp238/12TBWolf/RSPROX/TANDEMX_EDEM_GLOBAL/TANDEMX_EDEM_BATCHES"
to_dpath = "/media/ljp238/12TBWolf/RSPROX/TANDEMX_EDEM_GLOBAL/TANDEMX_EDEM_BATCHES_TAR/"


from_dpath = "/home/ljp238/Documents/ARCHIVE/OUT_TILES/EANA/"
#"/home/ljp238/Documents/ARCHIVE/OUT_TILES/TILES12"
#to_dpath = "/media/ljp238/12TBWolf/BACKUP/OUT_TILES/EANA"

#from_dpath = "/media/ljp238/12TBWolf/ARCHIEVE/WSF3D/data/"
from_dpath = "/media/ljp238/12TBWolf/ARCHIEVE/TDEMX/"

to_dpath ="/media/ljp238/12TBWolf/ARCHIEVE/TEMP/TDEMX12/"

if __name__ == "__main__":
    os.makedirs(to_dpath,exist_ok=True)
    tilenames = os.listdir(from_dpath)
    with ProcessPoolExecutor(10) as ppe:
        for i, tilename in enumerate(tilenames):
            #if i > 2: break
            fpath = os.path.join(from_dpath, tilename)
            tpath = os.path.join(to_dpath, tilename+".tar.gz")
            print(tpath)
            create_tarball(fpath,tpath)

            #ppe.submit(create_tarball,fpath,tpath)

    print('Done')
    send_notification(message='create_tarball DONE')