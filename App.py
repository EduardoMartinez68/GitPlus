#----this is for create the server----#
from flask import Flask, render_template, request, redirect,url_for, flash, session

#----this is for use the database----#
from dotenv import load_dotenv #this is for read the variable .env
from flask_mysqldb import MySQL
from src.lib.database.addDatabase import *
from src.lib.database.searchDatabase import *

#----this is for connection in live----#
from flask_socketio import SocketIO, emit, join_room, leave_room
import os 
import logging
import bcrypt

#from src.lib.config import Config
from src.lib.users.users import User, can_save_this_user, encrypt_password
from src.authentication.authentication import *

#initialize server  
app=Flask(__name__,template_folder='src/views/') #this is for start the app
pathApp=os.getcwd() #save the path of the app 


# load the variable of around from the file .env
load_dotenv()
mysql_host=os.getenv('MYSQL_HOST')
mysql_user=os.getenv('MYSQL_USER')
mysql_password=os.getenv('MYSQL_PASSWORD')
mysql_db=os.getenv('MYSQL_DB')

# config the connection with database mysql
app.config['MYSQL_HOST']=mysql_host
app.config['MYSQL_USER']=mysql_user
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']=mysql_db
db = MySQL(app)

#settings 
app.secret_key='mysecretkey' #initialization session
socketio = SocketIO(app)

#Configure the logger for SQLAlchemy
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def redirect_user(link):
    return redirect(url_for(link))

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


#--------------------------------------------links
@app.route('/')
def home():
    return render_template('links/web/login.html')

@app.route('/sign_up')
def sign_up():
    if unregistered_user(session):
        return render_template('links/web/signup.html')

@app.route('/login')
def login():
    if unregistered_user(session):
        return render_template('links/web/login.html')

@app.route('/sign_up_user', methods=['GET', 'POST'])
def sign_up_user():
    if request.method == 'POST':
        #get the data of the form 
        email = request.form['email']
        password = request.form['password']

        #we will waching if this user exist in the database 
        user=search_user_for_email(db,email)
        #(3, None, 'Soulss68', 'eduardoa4848@Outlook.es', '$2b$12$OArYWB6Y0sU7pGiemx6RsepOsEvWQKJrNKgxSlaUdfKSCeM7g.XwS', 0)
        if user:
            hashedPassword = user[4] #get the password
            if check_password(password,hashedPassword): #we will see if the password is equals 

                # if the user exist and the passwords are equals we going to save the data in the session
                username=user[2]
                session['logged_in'] = True
                session['username'] = username
                session['email'] = email 

                flash(f'Welcome {username}! ❤️', 'success')
                return redirect_user('profile')
            else:
                flash(f'The password not is equals 🤔', 'error')
        else:
            flash(f'This email not exist 🤔', 'error')

    return redirect_user('login')

@app.route('/sign_off')
def sign_off():
    session.pop('username', None)
    return redirect_user('login')

@app.route('/profile')
def profile():
    if registered_user(session):
        return render_template('links/git/tree.html')


@app.route('/tree')
def tree():
    if registered_user(session):
        return render_template('links/git/tree.html')


#--------------------------------------------add 
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        #get the data of the form 
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        email = request.form['email']
        terms = request.form['terms_and_conditions']

        #create a user 
        newUser=User(username,email,password1,password2,terms)

        #we will see if the data of the form is success 
        if can_save_this_user(newUser):
            #encrypt the password 
            newUser.password1=encrypt_password(password1)

            #we will see if could save the new user in the database 
            if add_new_user(db,newUser):
                flash('User added successfully! 🥳❤️', 'success')
                return redirect_user('tree')
            else:
                flash(f'The user not was added 😳', 'error')
    
    return redirect_user('login')


#-------------------------------------------this is for interact in live with the task
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('move_task')
def handle_move_task(data):
    print(f'Task moved: {data}')
    emit('task_moved', data, broadcast=True)


if __name__=='__main__':
    print('Connecting to the database...')
    try:
        with app.app_context():
            result = db.session.execute('SELECT * from "Company".users')
            print('Database connect')
    except Exception as e:
        print(f'Error connecting to the database: {e}')
    app.run(port=8000,debug=True)