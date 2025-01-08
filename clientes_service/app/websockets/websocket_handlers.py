from flask_socketio import SocketIO

socketio = SocketIO()

@socketio.on("connect")
def handle_connect():
    print("Cliente conectado")

@socketio.on("message")
def handle_message(message):
    print(f"Mensaje recibido: {message}")
    socketio.emit("response", {"message": "Mensaje recibido"})
