from flask import Blueprint, request, jsonify
import bcrypt
from database import get_connection
import jwt
import datetime
import sqlite3
import os
from dotenv import load_dotenv


auth_bp=Blueprint("auth",__name__)

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")


@auth_bp.route("/register", methods=["POST"])
def register():
    data=request.get_json()
    email=data.get("email")
    password=data.get("password")
    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400


    password_hash= bcrypt.hashpw(password.encode(),bcrypt.gensalt())

    conn= get_connection()
    try:
        conn.execute("INSERT INTO users (email , password_hash) VALUES (?,?)",(email,password_hash))
        conn.commit()


    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify({"error":"Email already registered"}),409
    
    conn.close()
    return jsonify({"message":"User registered"}),201
    

@auth_bp.route("/login",methods=["POST"])
def login():
    data=request.get_json()
    email=data.get("email")
    password=data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    conn=get_connection()
    user=conn.execute("SELECT * FROM users WHERE email = ?",(email,)).fetchone()
    conn.close()
    if user is None:
        return jsonify({"error":"Invalid email or password"}),401

    if bcrypt.checkpw(password.encode(),user["password_hash"]):

        token= jwt.encode(
            {
                "user_id": user["id"],
                "exp": datetime.datetime.utcnow()+datetime.timedelta(hours=2)
            } ,
            SECRET_KEY,
            algorithm= "HS256"

        )
        return jsonify({"token":token})
    else:
        return jsonify({"error": "Invalid email or password"}), 401





def get_current_user_id():
    auth_header=request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None


    try:
        token=auth_header.split(" ")[1]

        playload=jwt.decode(token,SECRET_KEY,algorithms= "HS256")
        return playload["user_id"]
    except InvalidTokenError:
        return None
