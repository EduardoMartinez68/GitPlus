from flask_mysqldb import MySQL

def add_new_user(db,user):
    try:
        # we will create the cursor and the query 
        cur = db.connection.cursor()
        cur.execute('INSERT INTO users (username,email,password) VALUES (%s,%s,%s)',
                    (user.username,user.email,user.password1))
        db.connection.commit() # save the new user in the database
        return True 
    except Exception as e:
        print(e)
        return False