const socket = io();

// Predefined list of teams
const teams = [
    "Elon A", "Elon B", "UNC A", "Team 4", "Team 5", "Team 6",
    "Team 7", "Team 8", "Team 9", "Team 10", "Team 11", "Team 12",
    "Team 13", "Team 14", "Team 15", "Team 16", "Team 17", "Team 18"
];

// Function to populate dropdowns
function populateTeamDropdowns() {
    let teamDropdowns = ["team1", "team2", "winner"];

    teamDropdowns.forEach(dropdownId => {
        let dropdown = document.getElementById(dropdownId);
        dropdown.innerHTML = '<option value="">Select Team</option>'; // Ensure the default option is included

        teams.forEach(team => {
            let option = document.createElement("option");
            option.value = team;
            option.textContent = team;
            dropdown.appendChild(option);
        });
    });
}

// Populate team dropdowns when page loads
document.addEventListener("DOMContentLoaded", populateTeamDropdowns);

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
