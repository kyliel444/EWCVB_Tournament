const socket = io();

// Listen for updates from the server and refresh the display
socket.on("refresh", function (data) {
    document.getElementById("phase").innerText = data.phase;
    let matchesDiv = document.getElementById("matches");
    match