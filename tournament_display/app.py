from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO
import json
import os

app = Flask(__name__, static_folder="static")
socketio = SocketIO(app)

# Path to tournament data file
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

# Save tournament data to JSON file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

tournament_data = load_data()

# Route for tournament display page
@app.route("/")
def index():
    return render_template("index.html", tournament=tournament_data)

# Route for admin panel page
@app.route("/admin")
def admin():
    return render_template("admin.html", tournament=tournament_data)

# Route to serve static files manually
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Route to update tournament data
@app.route("/update", methods=["POST"])
def update():
    global tournament_data
    data = request.json

    match_data = {
        "pool": data["pool"],
        "team1": data["team1"],
        "team2": data["team2"],
        "time": data["time"],
        "court": data["court"],
        "status": data["status"],
        "set1_score": data.get("set1_score", ""),
        "set2_score": data.get("set2_score", ""),
        "set3_score": data.get("set3_score", ""),
        "winner": data.get("winner", "")
    }

    tournament_data["matches"].append(match_data)
    save_data(tournament_data)

    socketio.emit("refresh", tournament_data)
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
