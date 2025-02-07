const express = require("express");
const http = require("http");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = new Server(server);

let messages = [];
let prices = [{ time: "10:00", open: 100, high: 110, low: 95, close: 105 }];

// Serve static files (your HTML file)
app.use(express.static(__dirname));

// WebSocket connection
io.on("connection", (socket) => {
    console.log("A user connected");

    // Send previous chat messages
    socket.emit("chatHistory", messages);
    
    // Send initial price data
    socket.emit("priceUpdate", prices);

    // Handle new chat messages
    socket.on("sendMessage", (data) => {
        messages.push(data);
        io.emit("newMessage", data);
    });

    // Simulate price updates every 3 seconds
    setInterval(() => {
        let lastPrice = prices[prices.length - 1].close;
        let newPrice = lastPrice + (Math.random() * 10 - 5);
        let high = newPrice + Math.random() * 5;
        let low = newPrice - Math.random() * 5;

        let newCandle = {
            time: new Date().toLocaleTimeString().slice(0, 5),
            open: lastPrice,
            high,
            low,
            close: newPrice,
        };

        prices.push(newCandle);
        if (prices.length > 8) prices.shift(); // Keep it short

        io.emit("priceUpdate", prices);
    }, 3000);
});

server.listen(3000, () => {
    console.log("Server running on http://localhost:3000");
});