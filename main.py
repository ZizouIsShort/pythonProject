from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("loginpage.html")

@app.route("/process_input", methods=["POST"])
def process_input():
    try:
        data = request.get_json()
        user_input = data["username"]
        user_input2 = data["password"]
        if not user_input:
            raise ValueError("Missing 'input' data in request body")

        print("Users email is :", user_input, "and password is", user_input2)
        response = {"message": "Input received successfully!"}
        return jsonify(response)

    except Exception as e:
        print(f"Error processing input: {e}")
        return jsonify({"error": str(e)}), 400


