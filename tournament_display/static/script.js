const socket = io();

// Predefined teams
const teams = [
    "Elon A", "Elon B", "UNC A", "UNC B", "UNC C", "VT A",
    "Team 7", "Team 8", "Team 9", "Team 10", "Team 11", "Team 12",
    "Team 13", "Team 14", "Team 15", "Team 16", "Team 17", "Team 18"
];

// Function to populate team dropdowns
function populateTeamDropdowns() {
    let team1Dropdown = document.getElementById("team1");
    let team2Dropdown = document.getElementById("team2");
    let winnerDropdown = document.getElementById("winner");

    teams.forEach(team => {
        let option1 = document.createElement("option");
        let option2 = document.createElement("option");
        let optionWinner = document.createElement("option");

        option1.value = option2.value = optionWinner.value = team;
        option1.textContent = option2.textContent = optionWinner.textContent = team;

        team1Dropdown.appendChild(option1);
        team2Dropdown.appendChild(option2);
        winnerDropdown.appendChild(optionWinner);
    });
}

// Populate dropdowns when page loads
document.addEventListener("DOMContentLoaded", populateTeamDropdowns);

// Listen for updates from the server and refresh the display
socket.on("refresh", function (data) {
    document.getElementById("phase").innerText = data.phase;
    let matchesDiv = document.getElementById("matches");
    matchesDiv.innerHTML = "";

    data.matches.forEach(match => {
        let matchDiv = document.createElement("div");
        matchDiv.classList.add("match");
        matchDiv.innerHTML = `<h3>${match.pool}: ${match.team1} vs ${match.team2}</h3>
                              <p><strong>Time:</strong> ${match.time}</p>
                              <p><strong>Court:</strong> ${match.court}</p>
                              <p><strong>Set 1:</strong> ${match.set1_score}</p>
                              <p><strong>Set 2:</strong> ${match.set2_score}</p>`;

        if (match.set3_score) {
            matchDiv.innerHTML += `<p><strong>Set 3:</strong> ${match.set3_score}</p>`;
        }

        matchDiv.innerHTML += `<p><strong>Winner:</strong> ${match.winner}</p>`;
        matchesDiv.appendChild(matchDiv);
    });
});

// Handle form submission for the admin panel
if (document.getElementById("updateForm")) {
    document.getElementById("updateForm").addEventListener("submit", function (e) {
        e.preventDefault();

        let matchData = {
            pool: document.getElementById("pool").value,
            team1: document.getElementById("team1").value,
            team2: document.getElementById("team2").value,
            time: document.getElementById("time").value,
            court: document.getElementById("court").value,
            set1_score: document.getElementById("set1_score").value,
            set2_score: document.getElementById("set2_score").value,
            set3_score: document.getElementById("set3_score").value || "",
            winner: document.getElementById("winner").value
        };

        fetch("/update", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(matchData)
        });

        document.getElementById("updateForm").reset();
    });
}
