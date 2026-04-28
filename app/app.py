from flask import Flask, request, jsonify, render_template
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="appuser",
        password="App@123",
        database="tasks_db",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks")
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

@app.route("/tasks", methods=["POST"])
def add_task():
    task = request.json.get("task")

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
    db.commit()
    db.close()

    return jsonify({"message": "Task added successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
