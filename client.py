"""
Client for a multi-client TCP chat application.

This script connects to the server, and then enters a loop
to allow the user to send messages interactively from the command line.
"""
import socket

# ==================================
# ===   CLIENT CONFIGURATION     ===
# ==================================
HEADER = 64  # Must match the server's header size.
PORT = 5050  # Must match the server's port.
FORMAT = 'utf-8'  # Must match the server's format.
MSG_DISCONNECT = "!Disconnect"  # Must match the server's disconnect message.
SERVER = "127.0.0.1"  # The server's IP address (localhost for local testing).
ADDR = (SERVER, PORT)

# ==================================
# ===    CLIENT SOCKET SETUP     ===
# ==================================
# Create a socket object (IPv4, TCP).
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Attempt to connect to the server.
try:
    client.connect(ADDR)
    print(f"[CONNECTED] Connected to server at {SERVER}:{PORT}")
# Handle the case where the server is not running.
except ConnectionRefusedError:
    print(f"[ERROR] Connection refused. Is the server running?")
    exit()  # Exit the script if connection fails.


# ==================================
# ===     SENDING FUNCTION       ===
# ==================================
def send(msg):
    """
    Handles the protocol for encoding and sending a message to the server.
    Returns True on success, False on failure.
    """
    try:
        # === THE COMMUNICATION PROTOCOL (CLIENT SIDE) ===
        # Step 1: Encode the message string into bytes.
        message = msg.encode(FORMAT)
        msg_length = len(message)

        # Step 2: Prepare the fixed-length header. First, encode the length into bytes.
        send_length = str(msg_length).encode(FORMAT)

        # Step 3: Pad the header with spaces to ensure it is exactly HEADER (64) bytes long.
        # This is crucial for the server to know exactly how many bytes to read for the header.
        send_length += b' ' * (HEADER - len(send_length))

        # Step 4: Send the header first.
        client.send(send_length)
        # Step 5: Then send the actual message.
        client.send(message)

        # Wait for and print the server's acknowledgment.
        server_response = client.recv(2048).decode(FORMAT)
        print(f"[SERVER] {server_response}")

    except (ConnectionResetError, BrokenPipeError):
        # These errors occur if the server closes the connection while we're trying to send.
        print("[ERROR] Connection to the server was lost.")
        return False
    return True


# ==================================
# === MAIN INTERACTIVE CHAT LOOP ===
# ==================================
print("You can now type messages. Type '!Disconnect' to quit.")

# This loop runs continuously, allowing the user to send multiple messages.
while True:
    # Wait for the user to type a message and press Enter.
    message = input("> ")

    # Ensure the user actually typed something before trying to send.
    if message:
        # Call the send function to transmit the message.
        # If send() returns False, it means the connection was lost, so we break the loop.
        if not send(message):
            break

        # If the user typed the disconnect message, we break the loop to exit the program.
        if message == MSG_DISCONNECT:
            break

# ==================================
# ===         CLEANUP            ===
# ==================================
print("[CLOSING] Connection closed.")
# It's good practice to explicitly close the socket when the program is finished.
client.close()