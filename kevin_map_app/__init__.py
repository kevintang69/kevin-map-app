from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coords.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://svpgomvwckxfor:28b9c719417b8b9d407c0d2c15f82188bbb9607ffe528527446a1661b0837f24@ec2-50-16-197-244.compute-1.amazonaws.com:5432/d8hl3grg73l3mt'

app.config['SECRET_KEY'] = '81b7d9a160566fc877bfd2a86d581cb4'

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager  = LoginManager(app)
login_manager.login_view = 'login'

from kevin_map_app import routes