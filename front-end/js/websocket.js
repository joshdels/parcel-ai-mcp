export function connectWebSocket(onMessage) {
  const socket = new WebSocket("ws://127.0.0.1:8000/ws");

  socket.onopen = () => {
    console.log("WebSocket connected");
  };

  socket.onmessage = (event) => {
    console.log("WebSocket message:", event.data);

    const message = JSON.parse(event.data);

    onMessage(message);
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };

  socket.onclose = () => {
    console.log("WebSocket disconnected");
  };

  return socket;
}

export function sendCommand(socket, command) {
  socket.send(JSON.stringify(command));
}
