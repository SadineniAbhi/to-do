from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))



@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


#@app.route("/joke")
@app.route("/datetime")
@app.route("/datetime", methods=["GET"])
def get_datetime():
    from datetime import datetime
    return jsonify({"datetime": datetime.now().isoformat()})

def joke():
    """Return a random joke as JSON."""
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "There are only 10 kinds of people in this world: those who know binary and those who don’t.",
        "I would tell you a UDP joke, but you might not get it.",
        "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'",
        "To understand recursion, you must first understand recursion.",
    ]
    return jsonify({"joke": random.choice(jokes)})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5002)
        db.create_all()
    db.create_all()
    app.run(debug=True, port=5002)
