from flask import Flask, render_template, request, redirect
# import the class from friend.py
from user import User
app = Flask(__name__)

@app.route("/users")
def read():
    users = User.get_all()
    return render_template("read.html", users=users)

@app.route("/users/new")
def create():
    return render_template("create.html")
    

@app.route("/users/new/add", methods=['POST'])
def add():
    print(request.form['first_name'])
    print(request.form['last_name'])
    print(request.form['email'])
    print(request.form['password'])

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"]
    }

    User.save(data)
    return redirect("/users")
            
if __name__ == "__main__":
    app.run(debug=True)
