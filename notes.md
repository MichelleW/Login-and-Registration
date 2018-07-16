          {% for friend in friends %}
          <div class="mx-auto col-6">

            <div>
              <span class="text-primary">First name:</span> {{friend['first_name']}}</div>
            <div>
              <span class="text-primary">Last name: </span>{{friend['last_name']}}</div>
            <div>
              <span class="text-primary">Occupation:</span> {{friend['occupation']}}</div>

          </div>
          {% endfor %} 




# def index():
#   # query the db to get value from friends table; store in all_friends array
#   all_friends = mysql.query_db("SELECT * FROM friends;")

#   return render_template('index.html', friends = all_friends)

@app.route('/login', methods=['POST'])
def create_friend():
  # query = "INSERT INTO friends (first_name, last_name, occupation, created_at,updated_at) VALUES (%(first_name)s, %(last_name)s,%(occupations)s, NOW(), NOW());"
  query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(occupation)s, NOW(), NOW());"
  data = {
    "first_name": request.form['fname'],
    "last_name": request.form['lname']
  }
  mysql.query_db(query, data)
  return redirect('/')


  <div class="col">
                <div class="form-group mt-5">
                    <h2>Login here!</h2>
                    <form action="/login" method="POST">
                      Email:
                    <input type="text" class="form-control mb-3" name="login_email">
                    Password:
                    <input type="text" class="form-control mb-3" name="loging_password">
                    <button class="btn btn-danger">Login</button>
                  </form>
                </div>
              </div>

# the rest of the form validation rules:
   if len(request.form['lname']) < 1:
        flash("Last name cannot be blank!")
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
    if len(request.form['password']) < 1:
        flash("Password cannot be blank!")
    if len(request.form['password']) < 2:
        flash("Password should be more than 8 characters")
        if request.form['password'].islower():
            flash("Password should have at least 1 uppercase letter ")
        if request.form['password'].isalpha():
            flash("Password should have at least 1 numeric value ")
    if len(request.form['confirmPassword']) < 1:
            flash("Please confirm password")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")

    elif request.form['password'] != request.form['confirmPassword']:
        flash("Password and Password Confirmation should match")
    

@app.route('/logged')
def logged():
    #only valid users can see this page, so we will track sessions here
    if 'submitted' in session and session['submitted'] == True:
        #search db again to get the user name that was registered
        return render_template('loggedin.html')
    else:
        return redirect("/")

@app.route('/login', methods=['Post'])
def login():
    # logic to validate user input
    if len(request.form['login_email']) < 1:
        flash("Please provide email")
    elif not EMAIL_REGEX.match(request.form['login_email']):
        flash("Invalid Email Address!")
    elif len(request.form['login_password']) < 1:
        flash("please login with your password")
    
    # see if username/email existin in db
    query = "SELECT * FROM users WHERE email= %(email)s;"
    data = { "email": request.form['login_email']}
    queryResults = mysql.query_db(query,data)
    print('HERE login email exist: ',queryResults)
    print('length: ',len(queryResults))
    print('result id: ',queryResults[0]['id'])
    if len(queryResults) > 0:
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, for this approach, we should have some logic to prevent duplicates of usernames when we create users
        if bcrypt.check_password_hash(queryResults[0]['password'],  request.form['login_password']):
            #if we get True after checking the password, we may put the use id in session
            session['userid'] = queryResults[0]['id']
            print('login email exist: ',queryResults)
            print('session id: ',session['userid'])
            return redirect("/success")
    # if user doen't exit
    print('you cannot be logged in')
    return redirect("/")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@app.route('/logged')
def logged():
    #only valid users can see this page, so we will track sessions here
    if 'submitted' in session and session['submitted'] == True:
        #search db again to get the user name that was registered
        return render_template('loggedin.html')
    else:
        return redirect("/")
