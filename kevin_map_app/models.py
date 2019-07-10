from kevin_map_app import db
from flask_login import UserMixin

class Run(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String, nullable= False)
    coord_string = db.Column(db.String,nullable =False)
    date_added = db.Column(db.DateTime, nullable = True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String, nullable= False , unique= True)
    password = db.Column(db.String, nullable= False)
    average_schedule = db.Column(db.Integer, nullable = False)
    average_lng = db.Column(db.Float, nullable = False)
    average_lat = db.Column(db.Float, nullable = False)
    total_runs = db.Column(db.Integer, nullable =False)
    total_points = db.Column(db.Integer, nullable = False)
    total_distance =  db.Column(db.Float, nullable= False)
    date_joined = db.Column(db.DateTime, nullable= False)
