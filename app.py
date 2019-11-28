from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

""" Instance app """
app = Flask(__name__)

""" Database location """
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/tasks.db"

""" Instance database """
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    done = db.Column(db.Boolean)


@app.route("/")
def home():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


@app.route("/tasks")
def get_tasks():
    return jsonify({"tasks"})


@app.route("/create_task", methods=["POST"])
def create_task():
    task = Task(task=request.form["task"], done=False)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/done_task/<string:id>")
def done_task(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete_task/<string:id>")
def delete_task(id):
    Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
    print(app)
