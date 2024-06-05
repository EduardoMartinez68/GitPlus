from flask_mysqldb import MySQL

def search_user_for_email(db,email):
    try:
        # we will create the cursor and the query 
        cur = db.connection.cursor()
        cur.execute(f"SELECT * from users WHERE email = '{email}'")
        user = cur.fetchone()
        return user 
    except Exception as e:
        print(e)
        return None 