from flask import  render_template, url_for ,redirect, flash, request, jsonify
from flask_login import  login_user,current_user, logout_user, login_required
import psycopg2
import datetime as dt

from kevin_map_app.forms import RegistrationForm, LoginForm
from kevin_map_app import bcrypt
from kevin_map_app import app
from kevin_map_app import login_manager
from kevin_map_app import db

from kevin_map_app.models import User, Run
from kevin_map_app.helper import remove_file, create_map


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods= ["POST",'GET'])
@app.route("/home", methods= ["POST",'GET'])
def home():
    return render_template('home.html', title = 'Homepage')


@app.route("/run", methods= ["POST",'GET'])
@login_required
def run():

    run_objects =list( Run.query.filter_by(username =  current_user.username ))
    info_dict_list = []
    for run_ob in run_objects:
        dic = {}
        name_of_run = create_map(run_ob.username, run_ob.date_added , run_ob.coord_string)
        dic['filename'] = name_of_run
        dic['id'] = run_ob.id
        dic['coord_string'] = run_ob.coord_string
        info_dict_list.append(dic)
    return render_template("mappage.html", imp = info_dict_list , title = 'look at those runs')




@app.route("/input_data", methods= ["POST",'GET'])
@login_required
def inp():
    if request.method =="POST":
        x = request.form
        new  = Run(username = current_user.username , coord_string=x["coord_string"], date_added = dt.datetime.utcnow())
        db.session.add(new)
        db.session.commit()
    
        
    return render_template("input_data.html" , title= 'Put in some data')

@app.route("/update", methods= ["POST"])
def update():
    data = request.form
    if data['action'] == 'delete':
        idnum = int(data['idnum'])
        obj = Run.query.filter_by(id=idnum).first()
        db.session.delete(obj)
        db.session.commit()

        remove_file(data['filename'])
        return jsonify({'result':'good'})



    elif data['action'] == 'change':
        idnum = int(data['idnum'])
        tob = dt.datetime.utcnow()
        obj = Run.query.filter_by(id=idnum).first()
        obj.coord_string = data['new_coord']
        obj.date_added = tob
        db.session.commit()

        remove_file( data['filename'])

        name_of_run = create_map(obj.username, tob, data['new_coord'])
        return jsonify( { 'newName' :  name_of_run }  )
        

@app.route("/viewruns")
@login_required
def viewruns():
    # every = Run.query.all()
    # for run in every:
    #     db.session.delete(run)
    # db.session.commit()

    if current_user.username == 'superkill13':
        all_runs = Run.query.all()
        l = []
        for run in all_runs:

            dic = {}
            dic['id'] = run.id
            dic['coords'] = run.coord_string
            dic['username'] = run.username
            l.append(dic)
        return render_template('view.html', imp = l)
    else:
        return "Not an approved user"

@app.route("/viewusers")
@login_required
def viewusers():

    if current_user.username == 'superkill13':
        all_users = User.query.all()
        l = []
        for user in all_users:

            dic = {}
            dic['id'] = user.id
            dic['username'] = user.username
            dic['password'] = user.password
            l.append(dic)
        return render_template('view.html', imp = l)
    else:
        return "Not an approved user"


@app.route("/register", methods = ['POST',"GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))


    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, password = hashed_password,
                    average_schedule=0, average_lng=0.0, average_lat = 0.0,
                    total_runs = 0, total_points = 0, total_distance = 0.0, 
                    date_joined = dt.datetime.utcnow()    )
        db.session.add(user)
        db.session.commit()



        flash("Account has been created")
        return redirect(url_for('login'))
    

    return render_template("registration.html", title = 'Register Now!', form=form)

@app.route("/login", methods = ['POST',"GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been logged in")
            return redirect(url_for('home'))
        else:
            flash("Username or password is incorrect")
    

    return render_template("login.html", title = 'Login Now!', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('login'))
