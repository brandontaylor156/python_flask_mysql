from flask import Flask, render_template, request, redirect
from user import User
app = Flask(__name__)

@app.route("/users")
def read():
    users = User.get_all()
    return render_template("read_all.html", users=users)

@app.route("/users/new")
def create():
    return render_template("create.html")

@app.route("/users/<int:user_id>")
def show(user_id):
    data = {
        "id": user_id
    }
    user = User.show_one(data)
    return render_template("read_one.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit(user_id):
    data = {
        "id": user_id
    }
    user = User.show_one(data)
    return render_template("edit.html", user=user)

@app.route("/users/<int:user_id>/update", methods=['POST'])
def update(user_id):
    user = User.update(request.form)
    print(request.form)
    return redirect(f"/users/{user_id}")

@app.route("/users/new/add", methods=['POST'])
def add():
    User.save(request.form)
    return redirect("/users")

@app.route("/users/<int:user_id>/delete")
def delete(user_id):
    data = {
        "id": user_id
    }
    User.delete(data)
    return redirect("/users")
            
if __name__ == "__main__":
    app.run(debug=True)
