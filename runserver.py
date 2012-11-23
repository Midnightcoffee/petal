'''
File: runserver.py
Date: 2012-11-23
Author: Drew Verlee
Description: script to run server on local machine. dated used replaced by 
foreman start
'''

# i suppose i just need the app
import os
from petalapp import app

# aren't necessary with gunicorn 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
