const socket = io();

socket.on("refresh", function (data) {
    document.getElementById("match").innerText = data.match;
    document.getElementById("score").innerText = data.score;
    document.getElementById("status").innerText = data.status;
});
