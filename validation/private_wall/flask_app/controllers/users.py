from crypt import methods
from flask_app import app, render_template, request, redirect, session, flash
from flask_app.models import user, message as message_module
from flask_bcrypt import Bcrypt
from pprint import pprint
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/register", methods=['POST'])
def insert_user():
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
    
    user_id = user.User.insert_user(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect("/user/dashboard")

@app.route("/user/dashboard")
def user_dashboard():

    data = {
        'id' : session['user_id']
    }
    user_info = user.User.select_all_user_attributes(data)

    user_info_dict = {}

    for message in user_info.messages:
        for friend in user_info.friends:
            if message.sender_id == friend.id:
                user_info_dict[message] = friend.first_name

    contact_list = user.User.select_all_users()

    for contact in contact_list:
        if contact.id == session['user_id']:
            contact_list.remove(contact)

    sent_messages = message_module.Message.select_all_sent_messages(data)

    return render_template("dashboard.html", user_info_dict = user_info_dict, contact_list = contact_list, sent_messages=sent_messages)

@app.route("/user/login", methods=['POST'])
def login_user():
    data = {
        "email": request.form['email'],
    }
    user_in_db = user.User.select_user_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password" , 'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", 'login')
        return redirect("/")

    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name

    return redirect("/user/dashboard")

@app.route("/user/message/<int:id>", methods=['POST'])
def insert_message(id):
    data = {
        'message': request.form['message'],
        'sender_id': session['user_id'],
        'receiver_id': id
    }
    new_message = message_module.Message.insert_message(data)
    pprint(new_message)
    return redirect("/user/dashboard")

@app.route("/message/delete/<int:id>")
def message_delete(id):
    data = {
        'id': id
    }
    message_module.Message.delete_message(data)
    return redirect("/user/dashboard")

@app.route("/user/logout")
def logout_user():
    session.clear()
    return redirect("/")