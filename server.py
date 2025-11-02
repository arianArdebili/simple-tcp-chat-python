"""
Server for a multi-client TCP chat application.

This script sets up a server that can listen for incoming connections,
and for each connection, it spawns a new thread to handle communication
with that client. This allows for multiple clients to be connected
and communicating simultaneously.
"""
import socket
import threading

# ==================================
# ===      CONFIGURATION         ===
# ==================================
HEADER = 64  # Defines a fixed-size header for messages, specifying the length of the upcoming message.
PORT = 5050  # The port number the server will listen on. Should be > 1023.
SERVER = "0.0.0.0"  # Special address meaning the server will listen on all available network interfaces.
ADDR = (SERVER, PORT)  # A tuple containing the IP and Port for the server to bind to.
FORMAT = "utf-8"  # The encoding format for messages.
MSG_DISCONNECT = "!Disconnect"  # A special message that signals the client wants to disconnect.

# ==================================
# ===      SERVER SETUP          ===
# ==================================
# Create a socket object.
# AF_INET specifies the address family (IPv4).
# SOCK_STREAM specifies the socket type (TCP).
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to our address and port. This "claims" the address so the OS
# knows to send incoming traffic for this port to our program.
server.bind(ADDR)


# ==================================
# ===   CLIENT HANDLER FUNCTION  ===
# ==================================
def handle_client(conn, addr):
    """
    This function is responsible for handling the communication for a single client.
    It runs in a separate thread for each connected client.
    """
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True

    # Main loop to receive messages from this specific client.
    while connected:
        try:
            # === THE COMMUNICATION PROTOCOL (SERVER SIDE) ===
            # Step 1: Receive the fixed-length header first. This is a blocking call.
            msg_length_header = conn.recv(HEADER).decode(FORMAT)

            # If the client disconnects cleanly, recv() will return an empty string.
            if not msg_length_header:
                connected = False
                continue

            # Step 2: Convert the header to an integer to get the actual message length.
            msg_length = int(msg_length_header)

            # Step 3: Receive the actual message, using the length we just determined.
            msg = conn.recv(msg_length).decode(FORMAT)

            # Check if the message is the disconnect command.
            if msg == MSG_DISCONNECT:
                connected = False

            # Log the received message to the server console.
            print(f"[{addr}] {msg}")

            # Send a confirmation message back to the client.
            conn.send("Message received".encode(FORMAT))

        # === ERROR HANDLING ===
        # This handles the case where a client forcibly closes the connection.
        except ConnectionResetError:
            print(f"[ERROR] Connection reset by {addr}. Client likely crashed.")
            connected = False
        # This handles the case where the header is not a valid number.
        except ValueError:
            print(f"[ERROR] Invalid header from {addr}. Forcing disconnect.")
            connected = False
        # Catch any other unexpected errors.
        except Exception as e:
            print(f"[UNEXPECTED ERROR] from {addr}: {e}")
            connected = False

    # === CLEANUP ===
    # This code runs after the loop breaks (i.e., the client has disconnected).
    print(f"[CLOSING] Closing connection for {addr}.")
    # IMPORTANT: We close 'conn' (the socket for this specific client), not 'server'.
    conn.close()


# ==================================
# ===   MAIN SERVER STARTUP      ===
# ==================================
def start():
    """Binds, listens, and accepts new connections, spinning off a new thread for each."""
    try:
        # Put the server into listening mode, ready to accept connections.
        server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")

        # Main loop to continuously accept new clients.
        while True:
            # This is a blocking call. It waits here until a new client connects.
            # When a client connects, it returns a new socket object 'conn' specific to that
            # client, and the client's address 'addr'.
            conn, addr = server.accept()

            # For each new connection, create and start a new thread.
            # The 'target' is the function that the thread will execute (handle_client).
            # The 'args' are the arguments to pass to that function.
            # This is the key to handling multiple clients simultaneously.
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

            # Print the number of active threads (minus the main server thread).
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    except OSError as e:
        print(f"[ERROR] Could not start server. Is another process using port {PORT}?")
        print(f"Details: {e}")
    except Exception as e:
        print(f"[UNEXPECTED ERROR] An error occurred: {e}")
    finally:
        # This block ensures the main server socket is closed if the server loop ever breaks.
        server.close()
        print("[SHUTDOWN] Server has been shut down.")


# ==================================
# ===      ENTRY POINT           ===
# ==================================
print("[STARTING] Server is starting...")
start()