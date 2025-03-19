from fileops import delete_folder_contents

folder_to_clean = "/media/ljp238/6tb1/Joseph/recovery_area/"
folder_names = ["FB_CHM", "CDEM_WBM", "GEOID", "ESAWC", "ETH_CHM_3deg_cogs",
                "LIDAR_DTM", "TDEMX12"]
for name in folder_names:
    folder_to_clean = f"/media/ljp238/12TBWolf/ARCHIEVE/TEMP/{name}"
    delete_folder_contents(folder_to_clean, verbose=True)