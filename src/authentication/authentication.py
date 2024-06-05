from flask import redirect,url_for

def redirect_user(link):
    return redirect(url_for(link))

def registered_user(session):
    if not 'logged_in' in session:
        return redirect_user('login')

    return True 

def unregistered_user(session):
    if 'logged_in' in session:
        return redirect(url_for('profile')) 

    return True
