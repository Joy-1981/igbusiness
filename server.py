<!DOCTYPE html>
<html lang="en">
<head>
    <title>IG Coin Exchange</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.4/socket.io.js"></script>
    <style>
        body { background: linear-gradient(135deg, #1a1a2e, #0f3460); color: white; font-family: Arial, sans-serif; text-align: center; }
        .container { background: #16213e; width: 80%; margin: 50px auto; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.2); }
        canvas { background: #0f3460; border-radius: 5px; }
        .chat-box { height: 200px; overflow-y: auto; border: 1px solid #f0a500; padding: 10px; background: #0f3460; text-align: left; }
        input, button { padding: 10px; margin: 5px; border: none; border-radius: 5px; }
        button { background: #f0a500; color: black; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>

    <div class="container">
        <h1>IG Coin Exchange</h1>
        <canvas id="chartCanvas" width="1200" height="500"></canvas>
        <h2>Live Chat</h2>
        <div class="chat-box" id="chatBox"></div>
        <input type="text" id="username" placeholder="Enter your username">
        <input type="text" id="message" placeholder="Type your message">
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        const socket = io.connect("http://localhost:5000");
        let ctx = document.getElementById("chartCanvas").getContext("2d");
        let prices = [];

        socket.on("chatHistory", (messages) => {
            messages.forEach(msg => addMessage(msg.username, msg.text));
        });

        socket.on("newMessage", (data) => {
            addMessage(data.username, data.text);
        });

        function sendMessage() {
            let username = document.getElementById("username").value;
            let message = document.getElementById("message").value;
            if (!username || !message) return alert("Enter both username and message");
            socket.emit("sendMessage", { username, text: message });
            document.getElementById("message").value = "";
        }

        function addMessage(username, text) {
            let chatBox = document.getElementById("chatBox");
            let newMessage = document.createElement("p");
            newMessage.innerHTML = <strong>${username}:</strong> ${text};
            chatBox.appendChild(newMessage);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        socket.on("priceUpdate", (newPrices) => {
            prices = newPrices;
            drawChart();
        });

        function drawChart() {
            ctx.clearRect(0, 0, 1200, 500);
            let x = 80;
            prices.forEach(data => {
                let color = data.close > data.open ? "green" : "red";
                ctx.fillStyle = color;
                ctx.fillRect(x, 500 - data.close * 3, 40, (data.close - data.open) * 3);
                ctx.strokeStyle = "white";
                ctx.beginPath();
                ctx.moveTo(x + 20, 500 - data.high * 3);
                ctx.lineTo(x + 20, 500 - data.low * 3);
                ctx.stroke();
                x += 150;
            });
        }
    </script>

</body>
</html>