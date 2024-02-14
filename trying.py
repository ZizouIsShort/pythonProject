import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ziyan@2005",
    database="testdb"
)
mycursor = mydb.cursor()
sql = 'INSERT INTO users (UID, email, password) VALUES (%s, "%s", "%s")'
val = (1, "zizouisshort@gmail.com", "zizou005")
mycursor.execute(sql, val)
mydb.commit()
mycursor.execute("SELECT * FROM users")
myresult = mycursor.fetchall()
print(myresult)