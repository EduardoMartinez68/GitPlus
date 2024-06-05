from flask import Flask, render_template, request, redirect,url_for, flash
import os 
from flask_sqlalchemy import SQLAlchemy


from src.lib.config import Config
from src.lib.users.users import User, save_a_new_user

app=Flask(__name__,template_folder='src/views/') #this is for start the app
pathApp=os.getcwd() #save the path of the app 

# config the connection with database
app.config.from_object(Config) 
db = SQLAlchemy(app)

#settings 
app.secret_key='mysecretkey' #initialization session


def redirect_user(link):
    return redirect(url_for(link))




@app.route('/')
def home():
    return render_template('links/web/login.html')

@app.route('/login')
def login():
    return render_template('links/web/login.html')

@app.route('/tree')
def tree():
    return render_template('links/git/tree.html')

@app.route('/add_user',methods=['POST'])
def add_user():
    if request.method=='POST':
        #get the data of the form 
        usaerName=request.form['username']
        password1=request.form['password1']
        password2=request.form['password2']
        email=request.form['email']
        term = request.form.get('terms_and_conditions') == 'on'
        
        #we create the user 
        newUser=User(usaerName,email,password1,password2,term)
        save_a_new_user(newUser)
    else:
        flash('ERROR to send the form', 'error')

    return redirect_user('home')

if __name__=='__main__':
    app.run(port=8000,debug=True)