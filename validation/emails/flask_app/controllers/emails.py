from flask_app import app, render_template, request, redirect, session
from flask_app.models import email

@app.route("/")
def index():
    return redirect("/emails")

@app.route("/emails")
def emails():
    return render_template("index.html")

@app.route("/email/insert", methods=['POST'])
def email_insert():
    if not email.Email.validate_email(request.form):
        return redirect("/")
    email.Email.insert_one(request.form)
    return redirect("/email/select/all")

@app.route("/email/select/all")
def email_select_all():
    emails = email.Email.select_all()
    return render_template("success.html", emails=emails)
