'''
File: tools.py
Date: 2012-11-07
Author: Drew Verlee
Description: contains upload_s3_chart and download_s3_chart
'''

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from petalapp import app
from petal.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,S3_BUCKET

from petalapp.graphing_tools.graph import plotpolar

#TODO refactor see aws imports
#TODO separate out functions, add try except
def upload_s3(destination_filename, data, acl="public-read"):
    """upload_s3 uploads a string to s3"""
    conn = boto.connect_s3(app.config["AWS_ACCESS_KEY_ID"],
            app.config["AWS_SECRET_ACCESS_KEY"])
    b = conn.get_bucket(app.config["S3_BUCKET"])

    file_name=plotpolar(data).getvalue()
    sml = b.new_key("/".join([app.config["S3_UPLOAD_DIRECTORY"],destination_filename]))
    sml.set_contents_from_string(file_name)

    # TODO investigate, Set the file's permissions.
    sml.set_acl(acl)

#TODO returning key, need a way to connect it to rest of code/add filename?
#def download_s3():
#    """download_s3 downloads from s3"""
#    conn = boto.connect_s3(app.config["AWS_ACCESS_KEY_ID"],
#            app.config["AWS_SECRET_ACCESS_KEY"])
#    b = conn.get_bucket(app.config["S3_BUCKET"])
#
#    k = Key(b)
#    return k
#

def download_s3():
    s3 = S3Connection(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY, is_secure=False)
    url = s3.generate_url(60, 'GET', bucket=S3_BUCKET, key="Your_FILE_KEY", force_http=True) #FIXME Your_FILE_KEY figure out how to get file
    return url #FIXME remember to filter url
