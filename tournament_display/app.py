from flask import Flask, render_template, request, jsonify, send_from_directory
import os

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
        "set1_score": data["set1_score"],
        "set2_score": data["set2_score"],
        "set3_score": data.get("set3_score", ""),  # Default to empty if not provided
        "winner": data["winner"]
    }

    tournament_data["matches"].append(match_data)

    # Save the updated data
    with open("data.json", "w") as f:
        json.dump(tournament_data, f, indent=4)

    # Notify all connected clients about the update
    socketio.emit("refresh", tournament_data)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    socketio.run(app, debug=True)
