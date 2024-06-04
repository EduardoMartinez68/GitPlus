from flask import flash
import bcrypt
class User():
    def __init__(self, userName, email,password1,password2,term):
        self.userName = userName
        self.email = email,
        self.password1=password1,
        self.password2=password2,
        self.term=term


def save_a_new_user(user):
    if not user.term:
        flash('You need accept the term and conditional', 'success') 
        return 
    
    #let's compare the passwords
    if not compare_password(user.password1,user.password2):
        flash('The password is incorrect', 'error')
        return 

    hashed_password = bcrypt.hashpw(user.password1.encode('utf-8'), bcrypt.gensalt()) #create the encrypt password 
    flash('User added successfully', 'success')

def compare_password(password1,password2):
    #let's compare the passwords and that the password not is null
    return password1==password2 and password1!=''

def add_user_database(usaerName, email, password):
    try:
        # we create a instance for the model User with the data of the form
        new_user = User(username=usaerName, email=email, password=password)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # we will waching if the user was added to the database with success
        user = User.query.filter_by(username=username).first()
        if user:
            return True 
        else:
            return False
    except Exception as e:
        print(f"Error al agregar usuario: {str(e)}")
        db.session.rollback()
        return False

