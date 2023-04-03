from flask import Flask
from flask import request
from flask import render_template
from flask_pymongo import PyMongo
from datetime import datetime
from datetime import timedelta
from bson.objectid import ObjectId
from flask import abort
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from flask_wtf.csrf import CSRFProtect
from flask import jsonify
import time
import math
import os
import platform




app = Flask(__name__)
csrf = CSRFProtect(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myweb" 
app.config["SECRET_KEY"] = "abcd"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
mongo = PyMongo(app)

BOARD_IMAGE_PATH = "C:\\Pictures"
BOARD_ATTACH_FILE_PATH = "C:\\Users\\user\\Desktop\\uploads"
ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])

app.config['BOARD_IMAGE_PATH'] = BOARD_IMAGE_PATH
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024
app.config['BOARD_ATTACH_FILE_PATH'] = BOARD_ATTACH_FILE_PATH

if not os.path.exists(app.config["BOARD_IMAGE_PATH"]):
    os.mkdir(app.config["BOARD_IMAGE_PATH"])
if not os.path.exists(app.config["BOARD_ATTACH_FILE_PATH"]):
    os.mkdir(app.config["BOARD_ATTACH_FILE_PATH"])

mongo = PyMongo(app)

from .common import login_required, allowed_file, rand_generator, check_filename, hash_password, check_password


from .filter import format_datetime
from . import board
from . import member

app.register_blueprint(board.blueprint)
app.register_blueprint(member.blueprint)

