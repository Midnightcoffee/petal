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
from petalapp.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,S3_BUCKET

from petalapp.graphing_tools.graph import plotpolar

#TODO refactor see aws imports
#TODO separate out functions, add try except
#TODO refactor path
def upload_s3(survey_header, organization,period, destination_filename, data, acl="public-read"):
    """upload_s3 uploads a string to s3"""
    conn = boto.connect_s3(app.config["AWS_ACCESS_KEY_ID"],
            app.config["AWS_SECRET_ACCESS_KEY"])
    b = conn.get_bucket(app.config["S3_BUCKET"])

    file_name=plotpolar(data).getvalue()
    sml = b.new_key("/".join([app.config["S3_UPLOAD_DIRECTORY"],
        survey_header, organization, period , destination_filename]))
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
#method described here:  http://www.givp.org/blog/2011/08/01/amazon-s3-expiring-urls-with-boto/
#def download_s3(file_key):
#    s3 = S3Connection(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY, is_secure=False)
#    url_w_extra = s3.generate_url(60, 'GET', bucket=S3_BUCKET, key=file_key, force_http=True) #FIXME Your_FILE_KEY figure out how to get file
#    #TODO make this more general somehow
#    file_title = url_w_extra[url_w_extra.find('.com/')+5:url_w_extra.find('?Signature')]
#    url = "https://s3.amazonaws.com/petalbucket/charts/" + file_title
#    return url_w_extra

#method here:http://jamiecurle.co.uk/blog/creating-expiring-link-s3/


def get_url_s3(file_path):
    s3conn = boto.connect_s3(app.config["AWS_ACCESS_KEY_ID"],app.config["AWS_SECRET_ACCESS_KEY"])
    bucket = s3conn.get_bucket(app.config["S3_BUCKET"])
    key = bucket.get_key('/'.join([app.config["S3_UPLOAD_DIRECTORY"], file_path]))
    seconds = 60*5
    url = key.generate_url(expires_in=seconds)
    return url

# then 
# g.url = download_s3('some_title')
# print(get_url_s3('staging/Pallative Care Index/Arizona Heart/test/2013'))

