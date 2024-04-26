from pprint import pprint
from flask import Flask, request, jsonify, render_template, url_for, redirect, session
import mysql.connector
import bcrypt
import requests
import json

apiKey = '6LAY8ZILRZS28YEI'
stocksUrl = 'https://www.alphavantage.co'

app = Flask(__name__)

app.secret_key = "ZiyansKey"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ziyan@2005",
    database="testdb"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT UNIQUE AUTO_INCREMENT, emailid VARCHAR(255) PRIMARY KEY, pass VARCHAR(255))")
mydb.commit()

@app.route("/")
def index():
    if "username" in session:
        return render_template("homepage.html")
    else:
        return render_template("loginpage.html")

@app.route("/trade", methods=["POST"])
def trade_stock():
    data = request.get_json()
    stock = data['stockName']
    action = data['action']
    quantity = float(data['quantity'])
    url = f'{stocksUrl}/query?function=TIME_SERIES_DAILY&symbol={stock}&interval=5min&apikey={apiKey}'
    r = requests.get(url)
    data = r.json()
    name = data['Meta Data']['2. Symbol']
    date = data['Meta Data']['3. Last Refreshed']
    p = float(data['Time Series (Daily)'][date]['4. close'])
    # data is already there
    total = p * quantity
    print(p)
    if action == 'b':
        print(2)
        mycursor.execute(f"SELECT stknm FROM trades WHERE stknm = '{stock}' AND bp = '{p}'")
        data = mycursor.fetchall()
        user_input = session.get('username')
        print(4)
        if not(len(data)):
            mycursor.execute(f"INSERT INTO trades (fkey ,stknm, pd, bp, bqty, btotal) VALUES ('{user_input}', '{stock}', '{date}', '{p}', {int(quantity)}, '{total}')")
            mydb.commit()
            print(3)
        else:
            print('Already exists')

        return jsonify({"status": "success", "message": "input received and trade executed"})

    elif action == 's':
        mycursor.execute(f"SELECT stknm FROM trades WHERE stknm = '{stock}'")
        data = mycursor.fetchall()
        if not(len(data)):
            print('Doesnt exists')
        else:
            mycursor.execute(f"INSERT INTO trades (sd, sp, sqty, stotal) VALUES ('{date}', '{p}', '{quantity}', '{total}'")
            mydb.commit()

        return jsonify({"status": "success", "message": "input received and trade executed"})

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
