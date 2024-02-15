from flask import Flask, request, jsonify, render_template
import mysql.connector

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
    try:
        data = request.get_json()
        user_input = data["username"]
        user_input2 = str(data["password"])
        if not user_input:
            raise ValueError("Missing 'input' data in request body")

        mycursor.execute(f"SELECT * FROM users WHERE emailid = '{user_input}'")
        data = mycursor.fetchall()

        if len(data) == 0:
            mycursor.execute(f"INSERT INTO users (emailid, pass) VALUES ('{user_input}', '{user_input2}')")
            mydb.commit()

            mycursor.execute(f"SELECT * FROM users WHERE emailid = '{user_input}'")
            data = mycursor.fetchall()

            return jsonify({
                "status": "success",
                "message": "New user created"
            })

        else:
            if data[0][2] == user_input2:
                return jsonify({
                    "status": "success",
                    "message": "Success"
                })
            else:
                return jsonify({
                    "status": "failure",
                    "message": "Incorrect Password"
                })

    except Exception as e:
        print(f"Error processing input: {e}")
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
