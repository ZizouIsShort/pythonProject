from flask import Flask, request, jsonify, render_template, url_for, redirect, session
import mysql.connector
import bcrypt

app = Flask(__name__)

app.secret_key = "ZiyansKey"


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ziyan@2005",
    database="testdb"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, emailid VARCHAR(255), pass VARCHAR(255))")
mydb.commit()

@app.route("/")
def index():
    if "username" in session:
        return render_template("homepage.html")
    else:
        return render_template("loginpage.html")


@app.route("/process_input", methods=["POST"])
def process_input():

    data = request.get_json()
    user_input = data["username"]
    user_input2 = data["password"]

    if not user_input:
        raise ValueError("Missing 'input' data in request body")

    mycursor.execute(f"SELECT pass FROM users WHERE emailid = '{user_input}'")
    data = mycursor.fetchall()

    if not len(data):
        pwBinary = user_input2.encode("utf-8")
        hashed_password = bcrypt.hashpw(pwBinary, bcrypt.gensalt())

        mycursor.execute(f"INSERT INTO users (emailid, pass) VALUES ('{user_input}', '{hashed_password.decode()}')", )
        print('yes')
        mydb.commit()
        session.permanent = True
        session["username"] = user_input
        return jsonify({"status": "success","message": "New user created"})

    else:
        storedPassword = data[0][0].encode("utf-8")
        if bcrypt.checkpw(user_input2.encode("utf-8"), storedPassword):
            print('gg')
            session.permanent = True
            session["username"] = user_input
            return jsonify({"status": "success","message": "success"})

        else:
            return jsonify({
                "status": "failure",
                "message": "Incorrect Password"
            })

if __name__ == "__main__":
    app.run(debug=True)
