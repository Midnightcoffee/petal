'''
File: db_temp_s3_mover.py
Date: 2012-11-15
Author: Drew Verlee
Description: just to help with temp move

'''
#TODO: rename this! its not a db...

from db_temp import organizations
from tools import upload_s3

def unpack_temp():
    for organization_name,mega_data in organizations.items():
        for i, data in enumerate(mega_data):
            assert(len(data) == 16)
            if i == 0:
                title_ext = "Baseline"
                which_quarter = ""
            else:
                title_ext = "Quarter"
                which_quarter = str(i + 2)
            upload_s3(title_ext+which_quarter+organization_name,(
                    title_ext, which_quarter, organization_name, data))

