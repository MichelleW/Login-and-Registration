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
        print('queryResults',queryResults)
        # if there's a match in db, user already exist
        if len(queryResults) > 0:
            flash("user email already exit")
        # if user/email doesn't exist in db, insert it into the db
        else:
            queryInsert = "INSERT INTO thisWall.users (firstname, lastname, email,password,created_at,updated_at) VALUES (%(fname)s, %(lname)s, %(email)s,%(password_hash)s,NOW(),NOW());"
            queryResults = mysql.query_db(queryInsert,data)
            # get the new user id and place it in session
            print("what is the query result after insert?",queryResults)
            session['userid'] = queryResults
            flash("You have been successfully registered!")
            return redirect('/success')

    return redirect('/')
    
@app.route('/login', methods=['POST'])
def login():
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = {"email":request.form['login_email']}
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
        # must map data according to the query_db function
        data = {
            'sessionid':session['userid']
        }
        # join two tables by usersid = messages.sender_id
        userQuery = "select * from messages join users on users.id = messages.sender_id WHERE recipient_id = %(sessionid)s;"
        queryUserInfo = "select * from users WHERE users.id = %(sessionid)s;"
        totalMsgSent = "select * from messages where messages.sender_id = %(sessionid)s;"
        userInfo = mysql.query_db(queryUserInfo, data)
        userQueryResult = mysql.query_db(userQuery, data)
        queryAllOtherUsers = "SELECT * FROM users WHERE id <> %(sessionid)s;"
    
        queryAllOtherUsersResults = mysql.query_db(queryAllOtherUsers,data)
        totalMsgSent= mysql.query_db(totalMsgSent,data)
        print('print query: ', userQueryResult)
        return render_template('welcome.html',userMessages = userQueryResult, userInfo=userInfo,queryAllOtherUsersResults=queryAllOtherUsersResults, totalMsgSent=totalMsgSent)
        return render_template('welcome.html',userInfo=userInfo)
    flash("please sign in")
    return redirect("/")

@app.route('/create_message',methods=['Post'])
def create_message():
    # send a query to get all user names  except for current user in session
    queryInsert = "INSERT INTO thisWall.messages (sender_id, recipient_id, messages,created_at,updated_at) VALUES (%(sessionid)s,%(recipient_id)s,%(messages)s, NOW(),NOW());"
    data = {
        'sessionid':session['userid'],
        'messages': request.form['message'],
        'recipient_id': request.form['recipient_id']
        }
    
     
    otherUsers = mysql.query_db(queryInsert,data)

    return redirect('/success')


@app.route('/delete/<id>')
def delete(id):
    data = {'deleteId' : id}
    query = "DELETE FROM messages WHERE messages.id = %(deleteId)s;"
    userQueryResult = mysql.query_db(query,data)
    flash('Message was deleted')
    return redirect('/success')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


#Pass in the database name here
mysql = connectToMySQL('thisWall')

# now, we may invoke the query_db method
# select the table from the db 
# print("all the users", mysql.query_db("SELECT * FROM messages;"))


if __name__=="__main__":
    app.run(debug=True)
