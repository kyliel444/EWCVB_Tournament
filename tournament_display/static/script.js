const socket = io();

// Listen for updates from the server and refresh the display
socket.on("refresh", function (data) {
    document.getElementById("phase").innerText = data.phase;
    let matchesDiv = document.getElementById("matches");
    matchesDiv.innerHTML = "";

    data.matches.forEach(match => {
        let matchDiv = document.createElement("div");
        matchDiv.classList.add("match");
        matchDiv.innerHTML = `<h3>${match.match}</h3>
                              <p><strong>Time:</strong> ${match.time}</p>
                              <p><strong>Court:</strong> ${match.court}</p>
                              <p><strong>Score:</strong> ${match.score}</p>
                              <p><strong>Winner:</strong> ${match.winner}</p>`;
        matchesDiv.appendChild(matchDiv);
    });
});

// Handle form submission for the admin panel
if (document.getElementById("updateForm")) {
    document.getElementById("updateForm").addEventListener("submit", function (e) {
        e.preventDefault();

        let match = document.getElementById("match").value;
        let time = document.getElementById("time").value;
        let court = document.getElementById("court").value;
        let score = document.getElementById("score").value;
        let winner = document.getElementById("winner").value;

        fetch("/update", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ match, time, court, score, winner })
        }).then(response => response.json())
          .then(data => console.log("Update successful:", data))
          .catch(error => console.error("Error:", error));

        // Clear form
        document.getElementById("updateForm").reset();
    });
}
