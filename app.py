from flask import Flask, request, jsonify
from database import init_db , get_connection
import time
from auth import auth_bp , get_current_user_id
app = Flask(__name__)
app.register_blueprint(auth_bp)


init_db()

@app.route("/")
def home():
    return "Hello, my first backend server!"

@app.route("/todos", methods=["GET"])
def get_todos():
    user_id= get_current_user_id()
    if user_id is None:
        return jsonify({"error":"Unauthorized"}),401
    conn=get_connection()
    rows = conn.execute("SELECT * FROM todos Where user_id=?",(user_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])



@app.route("/todos" , methods=["POST"])
def create_todo():
    user_id= get_current_user_id()
    if user_id is None:
        return jsonify({"error":"Unauthorized"}),401
    data = request.get_json()
    task=data.get("task")
    if not task:
        return jsonify({"error":"task is required"}),400


    conn=get_connection()
    exce = conn.execute("INSERT INTO todos (task , user_id) VALUES (?,?)",(task,user_id))
    conn.commit()
    new_id=exce.lastrowid
    conn.close()
    return jsonify({"id":new_id,"task":task,"done":False}), 201


@app.route("/todos/<int:todo_id>" , methods=["PUT"])
def update_todo(todo_id):
    user_id= get_current_user_id()
    if user_id is None:
        return jsonify({"error":"Unauthorized"}),401
    data= request.get_json()
    conn = get_connection()
    rows= conn.execute("SELECT * FROM todos WHERE id = ? and user_id=?",(todo_id,user_id)).fetchone()
    if rows is None:
        conn.close()
        return jsonify({"error":"Todo not found"}),404
    
    task=data.get("task", rows["task"])
    done=data.get("done", rows["done"])
    conn.execute("UPDATE todos SET task = ? , done = ? WHERE id= ? and user_id=?",(task,done,todo_id,user_id))
    conn.commit()
    conn.close()
    return jsonify({"id": todo_id, "task": task, "done": bool(done)})

    

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    user_id= get_current_user_id()
    if user_id is None:
        return jsonify({"error":"Unauthorized"}),401
    conn=get_connection()
    cursor= conn.execute("DELETE FROM todos WHERE id = ? and user_id=?",(todo_id,user_id))
    conn.commit()
    deleted= cursor.rowcount
    conn.close()

    if deleted == 0:
         return jsonify({"error":"Todo not found"}), 404

    return jsonify({"message": "Deleted"}),200

@app.route("/slow")
def slow():
    time.sleep(20)
    return "Done waiting 20 seconcds"

if __name__=="__main__":
   app.run(port=3000, debug=True)
