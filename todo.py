from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yuk_s/Desktop/TodoApp/todo.db'
db = SQLAlchemy(app)



@app.route("/")
def index():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list = todo_list)

@app.route("/add", methods=["POST"])
def add_todo():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def complete_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delete_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    db.create_all() # does not create already existing tables
    app.run(debug=True)
