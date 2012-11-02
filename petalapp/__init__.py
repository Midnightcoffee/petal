from flask import Flask

app = Flask(__name__)
app.config.from_object('defaultconfig')
app.config.from_envvar('PETAL_DEV')

from petalapp import views


