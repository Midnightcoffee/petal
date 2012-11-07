import boto
from boto.s3.key import Key
from petalapp import app

from graph import plotpolar

def upload_s3(num):
    destination_filename = 'achart'
    conn = boto.connect_s3(app.config["AWS_ACCESS_KEY_ID"], 
            app.config["AWS_SECRET_ACCESS_KEY"])
    b = conn.get_bucket(app.config["S3_BUCKET"])

    sml = b.new_key("/".join([app.config["S3_UPLOAD_DIRECTORY"],destination_filename]))
    sml.set_contents_from_string(plotpolar(num).getvalue())

# Set the file's permissions.
    sml.set_acl(acl)
    
def download_s3():
    destination_filename = 'achart'
    conn = boto.connect_s3(app.config["AWS_ACCESS_KEY_ID"], 
            app.config["AWS_SECRET_ACCESS_KEY"])
    b = conn.get_bucket(app.config["S3_BUCKET"])

    k = Key(b)
    return k

