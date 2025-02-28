from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Load or initialize tournament data
try:
    with open("data.json", "r") as f:
        tournament_data = json.load(f)
except FileNotFoundError:
    tournament_data = {
        "phase": "Pool Play",  # Can be "Pool Play", "Power Pools", or "Bracket Play"
        "matches": []
    }

@app.route("/")
def index():
    return render_template("index.html", tournament=tournament_data)

@app.route("/admin")
def admin():
    return render_template("admin.html", tournament=tournament_data)

@app.route("/update", met