const socket = io();

// Handle form submission
document.getElementById("updateForm").addEventListener("submit", function (e) {
    e.preventDefault();

    let matchData = {
        pool: document.getElementById("pool").value,
        team1: document.getElementById("team1").value,
        team2: document.getElementById("team2").value,
        time: document.getElementById("time").value,
        court: document.getElementById("court").value,
        status: document.getElementById("status").value,
        set1_score: document.getElementById("set1_score").value || "",
        set2_score: document.getElementById("set2_score").value || "",
        set3_score: document.getElementById("set3_score").value || "",
        winner: document.getElementById("winner").value || ""
    };

    // Send data to the backend
    fetch("/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(matchData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Match updated:", data);
        alert("Match successfully recorded!");
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error updating match.");
    });

    // Reset form after submission
    document.getElementById("updateForm").reset();
});
