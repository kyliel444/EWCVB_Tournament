from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Path to data.json
DATA_FILE = "data.json"

# Load or initialize tournament data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "phase": "Pool Play",
            "matches": [],
            "power_pools": [],
            "brackets": []
        }

# Save tournament data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

tournament_data = load_data()

@app.route("/")
def index():
    return render_template("index.html", tournament=tournament_data)

@app.route("/admin")
def admin():
    return render_template("admin.html", tournament=tournament_data)

@app.route("/update", methods=["POST"])
def update():
    """Receive match results and update the tournament."""
    global tournament_data
    data = request.json

    # Ensure all fields are included
    match_data = {
        "pool": data["pool"],
        "team1": data["team1"],
        "team2": data["team2"],
        "time": data["time"],
        "court": data["court"],
        "set1_score": data["set1_score"],
        "set2_score": data["set2_score"],
        "set3_score": data.get("set3_score", ""),  # Default to empty if missing
        "winner": data["winner"]
    }

    tournament_data["matches"].append(match_data)

    # Save updated data
    save_data(tournament_data)

    # Notify all clients via WebSocket
    socketio.emit("refresh", tournament_data)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    socketio.run(app, debug=True)
