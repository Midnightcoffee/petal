from uuid import uuid4
import boto
import os.path
from flask import current_app as app
from werkzeug import secure_filename

def s3_upload(source_file,acl='public-read'):
    source_filename = secure_filename(source_file.data.filename)
    source_extension = os.path.splitext(source_filename)[1]

    destination_filename = uuid4().hex + source_extension
     # Connect to S3

    conn = boto.connect_s3(app.config["AWS_ACCESS_KEY_ID"], app.config["AWS_SECRET_ACCESS_KEY"])
    b = conn.get_bucket(app.config["S3_BUCKET"])

    # Upload the File
    sml = b.new_key("/".join([app.config["S3_UPLOAD_DIRECTORY"],destination_filename]))
    sml.set_contents_from_string(source_file.data.readlines())

    # Set the file's permissions.
    sml.set_acl(acl)

    return destination_filename

