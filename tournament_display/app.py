from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Tournament Data (Example)
tournament_data = {
    "match": "Final - Team A vs Team B",
    "score": "0 - 0",
    "status": "Ongoing"
}

@app.route("/")
def index():
    return render_template("index.html", tournament=tournament_data)

# WebSocket event to update tournament info
@socketio.on("update_tournament")
def update_tournament(data):
    global tournament_data
    tournament_data.update(data)
    socketio.emit("refresh", tournament_data)  # Send update to all clients

if __name__ == "__main__":
    socketio.run(app, debug=True)
