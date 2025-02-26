from fileops import create_tarball
from concurrent.futures import ProcessPoolExecutor
import os
#from upaths import rsdata_dpath


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
if __name__ == '__main__':
    os.makedirs(to_dpath,exist_ok=True)
    tilenames = os.listdir(from_dpath)
    with ProcessPoolExecutor(10) as ppe:
        for i, tilename in enumerate(tilenames):
            #if i > 2: break
            fpath = os.path.join(from_dpath, tilename)
            tpath = os.path.join(to_dpath, tilename+'.tar.gz')
            print(tpath)

            ppe.submit(create_tarball,fpath,tpath)

    print('Done')