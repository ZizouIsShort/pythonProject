from flask import Flask, request, jsonify, render_template
import mysql.connector
import bcrypt

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ziyan@2005",
    database="testdb"
)

mycursor = mydb.cursor()

@app.route("/")
def index():
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
    else:
        storedPassword = data[0][0].encode("utf-8")
        if bcrypt.checkpw(user_input2.encode("utf-8"), storedPassword):
            return jsonify({
                            "status": "success",
                            "message": "Success"
                        })
        else:
                return jsonify({
                    "status": "failure",
                    "message": "Incorrect Password"
                })

if __name__ == "__main__":
    app.run(debug=True)
