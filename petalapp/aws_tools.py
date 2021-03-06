'''
File: tools.py
Date: 2012-11-07
Author: Drew Verlee
Description: contains upload_s3_chart and download_s3_chart
'''
import boto
from boto.s3.connection import OrdinaryCallingFormat
from petalapp import app
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


def get_url_s3(file_path):
    s3conn = boto.connect_s3(calling_format=OrdinaryCallingFormat)
    s3conn = boto.connect_s3(
    aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"])
    bucket = s3conn.get_bucket(app.config["S3_BUCKET"])
    key = bucket.get_key('/'.join([app.config["S3_UPLOAD_DIRECTORY"], file_path]))
    ten_years = 60 * 60 * 24 * 365 * 10
    url = key.generate_url(expires_in=ten_years)
    return url
