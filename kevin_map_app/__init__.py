from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

from boto.s3.connection import S3Connection
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coords.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bdkoiypkzsecqh:5738bdab0d6126cb8c73b4df5a44d136344025b8c4e88a5cc9ead0eb5a27b83a@ec2-174-129-227-80.compute-1.amazonaws.com:5432/drthp8eu9os3e'
#app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://qwcmmnxchztiww:adb5588045effd896b41f7bf1cae75877caa693095b09b9aa1a016f4c7057550@ec2-184-72-221-140.compute-1.amazonaws.com:5432/d34b0d0pvmdt1t'
app.config["SQLALCHEMY_DATABASE_URI"] =os.environ['DATABASE_URL']


app.config['SECRET_KEY'] = '81b7d9a160566fc877bfd2a86d581cb4'

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager  = LoginManager(app)
login_manager.login_view = 'login'

from kevin_map_app import routes