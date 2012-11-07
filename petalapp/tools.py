'''
File: tools.py
Date: 2012-11-07
Author: Drew Verlee
Description: contains upload_s3_chart and download_s3_chart
'''

import boto
from boto.s3.key import Key
from petalapp import app

from graph import plotpolar

#TODO separate out functions, add try except 
def upload_s3(destination_filename,file_name=plotpolar(num).getvalue(),
        acl="public-read"):
    """upload_s3 uploads a string to s3"""
    conn = boto.connect_s3(app.config["AWS_ACCESS_KEY_ID"],
            app.config["AWS_SECRET_ACCESS_KEY"])
    b = conn.get_bucket(app.config["S3_BUCKET"])

    sml = b.new_key("/".join([app.config["S3_UPLOAD_DIRECTORY"],destination_filename]))
    sml.set_contents_from_string(file_name)

    # TODO investigate, Set the file's permissions.
    sml.set_acl(acl)

#TODO returning key, need a way to connect it to rest of code/add filename?
def download_s3():
    """download_s3 downloads from s3"""
    conn = boto.connect_s3(app.config["AWS_ACCESS_KEY_ID"],
            app.config["AWS_SECRET_ACCESS_KEY"])
    b = conn.get_bucket(app.config["S3_BUCKET"])

    k = Key(b)
    return k


def upload_s3_chart
