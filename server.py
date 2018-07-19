# import Flask
from flask import Flask, render_template, redirect, request, session, flash
# import for password encryption
from flask_bcrypt import Bcrypt

# import Regex class from Flask for email validation
import re

# using pymSQLto connect mysql
from mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = "bigIsSecret!"
bcrypt = Bcrypt(app) 

@app.route('/', methods=['GET'])
def index():
    if 'visited' not in session:
        session['visited'] = 0
    if 'userid' not in session:
        session['userid'] = 0
        session['visited'] +=1
        print('user id:',session['userid'], 'visited:', session['visited'])
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    # check blank fields
    if len(request.form['fname']) < 2:
        flash("First name should have at least 2 characters")
    elif len(request.form['lname']) < 2:
        flash("Last name should have at least 2 characters")
    elif len(request.form['email']) < 1:
        flash("Email cannot be blank!")
    elif not EMAIL_REGEX.match(request.form['email']):
            flash("Invalid Email Address!")
    elif len(request.form['password']) < 2 or len(request.form['password']) < 8:
            flash("Password should be more than 8 characters")
    elif request.form['password'].islower():
        flash("Password should have at least 1 uppercase letter ")
    elif request.form['password'].isalpha():
        flash("Password should have at least 1 numeric value ")
    elif len(request.form['confirmPassword']) < 2:
            flash("Please confirm password")

    else:
        # create password hash
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print('hashed pw',pw_hash)
        query = "SELECT * FROM users WHERE email= %(email)s;"
        data = {
            "email":request.form['email'],
            "fname":request.form['fname'],
            "lname": request.form['lname'],
            "password_hash": pw_hash,
            }
        # store the result (an array) from talking to the database in the variable 
        queryResults = mysql.query_db(query,data)
        # if there's a match in db, user already exist
        if len(queryResults) > 0:
            flash("user email already exit")
        #if user/email doesn't exist in db, insert it into the db
        else:
            query = "INSERT INTO customerleads.users (firstname, lastname, email,password) VALUES (%(fname)s, %(lname)s, %(email)s,%(password_hash)s);"
            queryResults = mysql.query_db(query,data)
            # get the new user id and place it in session
            print("what is the query result after insert?",queryResults)
            session['userid'] = queryResults
            flash("You have been successfully registered!")
            return redirect('/success')

    return redirect('/')


# login route

# @app.route('/login', methods=['Post'])
# def login():
#     # see if username/email existin in db
#     query = "SELECT * FROM users WHERE email= %(email)s;"
#     data = { "email": request.form['login_email']}
#     queryResults = mysql.query_db(query,data)
#     if queryResults:
#         print('yes queryResults',queryResults)
#         # assuming we only have one user with this username, the user would be first in the list we get back
#         # of course, for this approach, we should have some logic to prevent duplicates of usernames when we create users
#         # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
#         if bcrypt.check_password_hash(queryResults[0]['password'], request.form['login_password']):
#             # if we get True after checking the password, we may put the user id in session
#             # never render on a post, always redirect!
#             return redirect('/success')
#         # if we didn't find anything in the database by searching by username or if the passwords don't match,
#         # flash an error message and redirect back to a safe route
#         flash("You could not be logged in")
#         return redirect("/")

@app.route('/login', methods=['POST'])
def login():
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form["login_email"] }
    result = mysql.query_db(query, data)
    print('logged and query result: ',result)
    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['login_password']):
            session['userid'] = result[0]['id']
            return redirect('/success')
    flash("You could not be logged in")
    return redirect("/")

@app.route('/success')
def success():
    #only valid users can see this page, so we will track sessions here
    if session['userid']:
        print('logged in success route for userid: ',session['userid'])
        return render_template('welcome.html')
    flash("please sign in")
    return redirect("/")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


#Pass in the database name here
mysql = connectToMySQL('customerleads')

# now, we may invoke the query_db method
# select the table from the db 
# print("all the users", mysql.query_db("SELECT * FROM users;"))


if __name__=="__main__":
    app.run(debug=True)
