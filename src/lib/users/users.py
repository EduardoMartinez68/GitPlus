from flask import flash
import bcrypt

class User():
    def __init__(self, username, email,password1,password2,term):
        self.username = username
        self.email = email,
        self.password1=password1,
        self.password2=password2,
        self.term=term

def can_save_this_user(user):
    if not user.term:
        flash('You need accept the term and conditional', 'success') 
        return False
    
    #let's compare the passwords
    if not compare_password(user.password1,user.password2):
        flash('The password is incorrect', 'error')
        return False

    return True

def compare_password(password1,password2):
    #let's compare the passwords and that the password not is null
    return password1==password2 and password1!=''

def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) #create the encrypt password 

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
