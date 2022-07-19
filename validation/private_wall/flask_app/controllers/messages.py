from flask_app import app, render_template, request, redirect, session, flash
from flask_app.models import message as message_module

@app.route("/user/message/<int:id>", methods=['POST'])
def insert_message(id):
    if 'user_id' not in session:
        return redirect("/")

    if not message_module.Message.validate_message(request.form):
        return redirect("/user/dashboard")

    data = {
        'message': request.form['message'],
        'sender_id': session['user_id'],
        'receiver_id': id
    }
    new_message = message_module.Message.insert_message(data)
    return redirect("/user/dashboard")

@app.route("/message/delete/<int:id>")
def message_delete(id):
    if 'user_id' not in session:
        return redirect("/")
    data = {
        'id': id
    }
    message_module.Message.delete_message(data)
    return redirect("/user/dashboard")