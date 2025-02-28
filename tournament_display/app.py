from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from flask_socketio import SocketIO

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(debug=True)


# Load or initialize tournament data
try:
    with open("data.json", "r") as f:
        tournament_data = json.load(f)
except FileNotFoundError:
    tournament_data = {
        "phase": "Pool Play",
        "matches": [],
        "power_pools": [],
        "brackets": []
    }


@app.route("/update", methods=["POST"])
def update():
    """Receive match results and update the tournament."""
    global tournament_data
    data = request.json

    # Add the new match result with the new structure
    match_data = {
        "pool": data["pool"],
        "team1": data["team1"],
        "team2": data["team2"],
        "time": data["time"],
        "court": data["court"],
        