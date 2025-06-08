from flask import Flask, jsonify, request, redirect, url_for, render_template_string
from flask_cors import CORS
import random
import base64
import json
from flask_cors import cross_origin


app = Flask(__name__)
# CORS(app, origins=["https://not-matiks.hrishk.me", "https://not-matiks-rdbj-6lr2sftol-hrishi-008s-projects.vercel.app"], supports_credentials=True)


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
@cross_origin(origins=["https://not-matiks.hrishk.me/"])
def get_question():
    q = random_addn_question()
    return jsonify({"question": q["question"], "token": q["token"]})

@app.route("/check", methods=["POST"])
@cross_origin(origins=["https://not-matiks.hrishk.me/"])
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

@app.route("/")
@cross_origin(origins=["https://not-matiks.hrishk.me/"])
def welcome():
    welcome_html = """
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Welcome to Not-Matiks</title>
        <link rel="icon" type="image/png" href="Frontend\public\favi.png">
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #0F0F0F;
                color: #F2F2F2;
                text-align: center;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .logo {
                width: 150px;
                height: auto;
                margin-bottom: 20px;
            }
            h1 {
                font-size: 2.5rem;
                margin-bottom: 1rem;
            }
            p {
                font-size: 1.2rem;
                margin-bottom: 2rem;
            }
            a {
                display: inline-block;
                padding: 0.8rem 1.5rem;
                font-size: 1rem;
                color: #0F0F0F;
                background-color: #F2F2F2;
                text-decoration: none;
                border-radius: 5px;
                transition: background-color 0.3s;
            }
            a:hover {
                background-color: #E0E0E0;
            }
        </style>
    </head>
    <body>
        <img src='/static/favi.png' alt='Not-Matiks Logo' class='logo'>
        <h1>Welcome to Not-Matiks</h1>
        <p>Your ultimate math challenge awaits!</p>
        <a href='https://not-matiks.hrishk.me/'>Go to Questions</a>
    </body>
    </html>
    """
    return render_template_string(welcome_html)

# if __name__ == "__main__":
#     app.run(debug=True)
