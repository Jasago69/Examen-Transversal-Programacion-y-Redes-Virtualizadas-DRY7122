import pyotp
import sqlite3
import hashlib
import uuid
from flask import Flask, request

app = Flask(__name__)

db_name = 'test.db'

@app.route('/')
def index():
    return 'Welcome to the hands-on lab for an evolution of password systems!'

@app.route('/signup', methods=['POST'])
def signup():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USERS
           (ID        TEXT    PRIMARY KEY NOT NULL,
            USERNAME  TEXT    NOT NULL,
            HASH      TEXT    NOT NULL);''')
    conn.commit()
    try:
        username = request.form['username']
        password = request.form['password']
        hash_value = hashlib.sha256(password.encode()).hexdigest()
        c.execute("INSERT INTO USERS (ID, USERNAME, HASH) "
                  "VALUES ('{0}', '{1}', '{2}')".format(uuid.uuid4().hex, username, hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Username has already been registered."
    return "Signup success"

def verify_user(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT HASH FROM USERS WHERE USERNAME = '{0}'".format(username)
    c.execute(query)
    record = c.fetchone()
    conn.close()
    if not record:
        return False
    return record[0] == hashlib.sha256(password.encode()).hexdigest()

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == "Jonathan Aseña" and password == "123456":
        return "Login success"
    elif username == "Rodrigo Oyarce" and password == "123456":
        return "Login success"
    else:
        return "Invalid username/password"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9500)