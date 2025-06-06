from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import base64
import json

app = Flask(__name__)
CORS(app)

def random_addn_question():
    n1 = random.randint(1, 100)
    n2 = random.randint(1, 100)
    operator = random.choice(['+', '-'])
    question = f"{n1} {operator} {n2}"
    answer = eval(question)
    # Encode the answer in a token (stateless)
    token_data = {"answer": answer}
    token = base64.urlsafe_b64encode(json.dumps(token_data).encode()).decode()
    return dict(question=question, token=token)

@app.route("/question", methods=["GET"])
def get_question():
    q = random_addn_question()
    return jsonify({"question": q["question"], "token": q["token"]})

@app.route("/check", methods=["POST"])
def check_answer():
    data = request.get_json()
    user_answer = data.get("answer")
    token = data.get("token")
    try:
        token_data = json.loads(base64.urlsafe_b64decode(token.encode()).decode())
        correct_answer = token_data["answer"]
        correct = (str(user_answer) == str(correct_answer))
    except Exception:
        return jsonify({"error": "Invalid token"}), 400

    # Generate new question for next round
    q = random_addn_question()
    return jsonify({
        "correct": correct,
        "new_question": q["question"],
        "token": q["token"]
    })

if __name__ == "__main__":
    app.run(debug=True)
