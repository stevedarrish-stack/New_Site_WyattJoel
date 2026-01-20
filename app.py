
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Allow both local dev and production frontend
CORS(app, origins=[
    "https://stevedarrish-stack.github.io",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
])



@app.route('/inquiry', methods=['POST'])
def inquiry():
    name = request.form.get('name')
    email = request.form.get('email')
    topic = request.form.get('topic')
    message = request.form.get('message')
    print(f"Received inquiry: {name}, {email}, {topic}, {message}")
    # TODO: Send email or store inquiry as needed
    return jsonify({"success": True, "message": "Thank you for your inquiry!"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

  