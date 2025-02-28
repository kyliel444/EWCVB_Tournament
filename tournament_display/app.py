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
        "phase": "Pool Play",
        "matches": [],
        "power_pools": [],
        "brackets": []
    }

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

    # Add the new match result with time and court number
    tournament_data["matches"].append({
        "match": data["match"],
        "time": data["time"],
        "court": data["court"],
        "score": data["score"],
        "winner": data["winner"]
    })

    # Save the data
    with open("data.json", "w") as f:
        json.dump(tournament_data, f, indent=4)

    # Notify clients about the update
    socketio.emit("refresh", tournament_data)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    socketio.run(app, debug=True)
