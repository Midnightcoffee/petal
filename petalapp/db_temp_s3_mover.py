'''
File: db_temp_s3_mover.py
Date: 2012-11-15
Author: Drew Verlee
Description: just to help with temp move

'''
#TODO: rename this! its not a db...

from db_temp import hospitals
from tools import upload_s3

def unpack_temp():
    for hospital_name,mega_data in hospitals.items():
        for i, data in enumerate(mega_data):
            if i == 0:
                title_ext = "Baseline"
                which_quarter = ""
            else:
                title_ext = "Quarter"
                which_quarter = str(i + 2)
            upload_s3(title_ext+which_quarter+hospital_name,(
                    title_ext, which_quarter, hospital_name, data))

unpack_temp()
