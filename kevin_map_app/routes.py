from flask import  render_template, url_for ,redirect, flash, request, jsonify, send_from_directory
from flask_login import  login_user,current_user, logout_user, login_required
import psycopg2
import datetime as dt

from kevin_map_app.forms import RegistrationForm, LoginForm
from kevin_map_app import bcrypt
from kevin_map_app import app
from kevin_map_app import login_manager
from kevin_map_app import db


from kevin_map_app.models import User, Run
from kevin_map_app.helper import get_time_string, create_time_object, remove_file, create_map ,zeropad, check_input, return_file_path, clean_string


NAV_DICTS = {'s13':  [{'name': 'All Runs','link': '/viewruns'},{'name': 'All Users','link': '/viewusers'},{'name': 'Input','link': '/input_data'},{'name': 'View','link': '/run'},{'name': 'Logout','link': '/logout'}] ,    'logged_in': [{'name': 'Input','link': '/input_data'},{'name': 'View','link': '/run'},{'name': 'Logout','link': '/logout'}] , 'logged_out':[{'name':'Login', 'link':'/login'}, {'name': 'Register', 'link':'/register'}]  }



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(return_file_path('') ,'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/", methods= ["POST",'GET'])
@app.route("/home", methods= ["POST",'GET'])
def home():

    if current_user.is_authenticated:
        if current_user.username == 'superkill13':
            nav = NAV_DICTS['s13']
        else:
            nav = NAV_DICTS['logged_in']
    else:
        nav = NAV_DICTS['logged_out']

    return render_template('home.html', title = 'Homepage', nav= nav)


@app.route("/run", methods= ["POST",'GET'])
@login_required
def run():

    if current_user.is_authenticated:
        if current_user.username == 'superkill13':
            nav = NAV_DICTS['s13']
        else:
            nav = NAV_DICTS['logged_in']
    else:
        nav = NAV_DICTS['logged_out']

    run_objects =list( Run.query.filter_by(username =  current_user.username ))
    info_dict_list = []
    for run_ob in run_objects:
        dic = {}
        name_of_run = create_map(run_ob.username, run_ob.date_added , run_ob.coord_string)
        dic['filename'] = name_of_run
        dic['id'] = run_ob.id
        dic['coord_string'] = run_ob.coord_string
        tob = run_ob.date_added

        dic['date'] = f"{zeropad(tob.year)}-{zeropad(tob.month)}-{zeropad(tob.day)}"

        dic['hour'] = tob.hour
        dic['minute']= tob.minute
        dic['second']= tob.second
        info_dict_list.append(dic)
    return render_template("mappage.html", imp = info_dict_list , title = 'look at those runs',nav=nav  )




@app.route("/input_data", methods= ["POST",'GET'])
@login_required
def inp():

    if current_user.is_authenticated:
        if current_user.username == 'superkill13':
            nav = NAV_DICTS['s13']
        else:
            nav = NAV_DICTS['logged_in']
    else:
        nav = NAV_DICTS['logged_out']


    return render_template("input_data.html" , title= 'Put in some data',nav=nav)

@app.route("/update", methods= ["POST"])
def update():
    data = request.form

    if data['action']  == 'add':
        if check_input(data['coord_string']) == False:
            flash("Invalid coordinates input")
            return redirect(url_for('inp'))


        if 'default' in data:
            ori_time_ob = dt.datetime.utcnow()
            time_ob = create_time_object(get_time_string(ori_time_ob))
        else:
            year = int(data['date'][0:4])
            day = int(data['date'][8:10])
            month = int(data['date'][5:7])
            time_ob = dt.datetime( year,month,day,int(data['hour']),int(data['minute']),int(data['second'] ))  

        existing_times = Run.query.filter_by(date_added = time_ob)
        if existing_times.count()!=0:
            flash("Duplicate time input")
            return redirect(url_for('inp'))

        new_run = Run(username= current_user.username , date_added = time_ob,coord_string= clean_string(data['coord_string'])  )
        db.session.add(new_run)
        db.session.commit()
        flash("Data has been entered")

        return redirect(url_for('inp'))

    elif data['action'] == 'delete':
        idnum = int(data['idnum'])
        obj = Run.query.filter_by(id=idnum).first()
        db.session.delete(obj)
        db.session.commit()

        remove_file(data['filename'])
        return jsonify({'result':'good'})



    elif data['action'] == 'change':


        if check_input(data['new_coord']) == False:
            return jsonify({'result':'bad'})

       
        idnum = int(data['idnum'])
        new_time_string = data['new_time_string']


        existing_times = Run.query.filter_by(date_added = create_time_object(new_time_string))
        if existing_times.count()==0: #no duplicate times


            obj = Run.query.filter_by(id=idnum).first()
            old_time_string = get_time_string( obj.date_added)
            old_coord = clean_string( obj.coord_string ) 




            if old_coord.strip() != data['new_coord'].strip() or old_time_string != new_time_string  or clean_string(data['new_coord']) != old_coord :

                obj.coord_string =  clean_string(data['new_coord'])
                obj.date_added = create_time_object(new_time_string)
                db.session.commit()

                remove_file( data['filename'])

                name_of_run = create_map(obj.username, create_time_object(new_time_string), clean_string(data['new_coord']))
                return jsonify( { 'newName' :  name_of_run , 'result': 'good'}  )
    return jsonify({'result':'bad'})


@app.route("/delete_all")
@login_required
def delete_all():


    if current_user.username == 'superkill13':
        every = Run.query.all()
        for run in every:
            db.session.delete(run)
        db.session.commit()

        return "All entries deleted"
    else:
        return "Not an approved user"
        

@app.route("/viewruns")
@login_required
def viewruns():
    if current_user.is_authenticated:
        if current_user.username == 'superkill13':
            nav = NAV_DICTS['s13']
        else:
            nav = NAV_DICTS['logged_in']
    else:
        nav = NAV_DICTS['logged_out']


    if current_user.username == 'superkill13':
        all_runs = Run.query.all()
        l = []
        for run in all_runs:

            dic = {}
            dic['ID'] = run.id
            
            dic['Username'] = run.username
            dic['Coordinates'] = run.coord_string
            dic['Date'] = get_time_string(run.date_added)
            
            l.append(dic)
 
        return render_template('view.html', imp = l,nav=nav  )
    else:
        return "Not an approved user"

@app.route("/viewusers")
@login_required
def viewusers():

    if current_user.is_authenticated:
        if current_user.username == 'superkill13':
            nav = NAV_DICTS['s13']
        else:
            nav = NAV_DICTS['logged_in']
    else:
        nav = NAV_DICTS['logged_out']

    if current_user.username == 'superkill13':
        all_users = User.query.all()
        l = []
        for user in all_users:

            dic = {}

            dic['ID'] = user.id
            dic['Username'] = user.username
            dic['Average-Schedule'] = user.average_schedule
            dic['Average-Lat'] = user.average_lat
            dic['Average-Lng'] = user.average_lng
            dic['Total-Runs'] = user.total_runs
            dic['Total-Points'] = user.total_points
            dic['Total-Distance'] = user.total_distance
            dic['Date-Joined'] = get_time_string(user.date_joined) 

            l.append(dic)
        return render_template('view.html', imp = l,nav=nav  )
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

#