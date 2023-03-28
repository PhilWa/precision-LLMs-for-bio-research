from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from get_answer import get_answer
from enhance_answer import enhance_prompt
from references import add_references, add_ref
from connect_openai.connect_openai import chatbot_response
import markdown
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///votes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text, nullable=False)
    output_text = db.Column(db.Text, nullable=False)
    vote = db.Column(db.String(10), nullable=False)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process_text():
    text_input = request.form["text_input"]
    if 'biogpt' in text_input.lower():
        value = enhance_prompt(text_input)
        value = value.replace('biogpt', "")
        ans = get_answer(value)[0].get("generated_text")

    else:
        value = enhance_prompt(text_input)
        ans = chatbot_response(value)
    
    ans += add_ref(ans, top_n=2)

    markdown_text = markdown.markdown(ans)
    markdown_text = markdown_text.replace("<a ", '<a target="_blank" ')
    return jsonify({"result": markdown_text})


@app.route("/vote", methods=["POST"])
def save_vote():
    input_text = request.form["input_text"]
    output_text = request.form["output_text"]
    vote = request.form["vote"]

    new_vote = Vote(input_text=input_text, output_text=output_text, vote=vote)
    db.session.add(new_vote)
    db.session.commit()

    return jsonify({"message": "Vote saved."})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
