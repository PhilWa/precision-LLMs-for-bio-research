from flask import Flask, render_template, request, jsonify
import random
import game_of_life_logic as logic

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/update", methods=["POST"])
def update():
    grid = request.json["grid"]
    new_grid = logic.update_grid(grid)
    return jsonify(new_grid)


if __name__ == "__main__":
    app.run(debug=True)
