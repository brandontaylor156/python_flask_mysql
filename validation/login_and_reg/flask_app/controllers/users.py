from flask_app import app, render_template, request, redirect, session, flash
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/register", methods=['POST'])
def user_insert():
    if not user.User.validate_user(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    
    user_id = user.User.insert_one(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect("/user/dashboard")

@app.route("/user/dashboard")
def user_dashboard():
    if 'user_id' not in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.route("/user/login", methods=['POST'])
def user_login():
    data = {
        "email": request.form['email'],
    }
    user_in_db = user.User.select_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password" , 'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", 'login')
        return redirect("/")

    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name

    return redirect("/user/dashboard")

@app.route("/user/logout")
def user_logout():
    session.clear()
    return redirect("/")