# Python Socket Chat

A simple, command-line based, multi-client TCP chat application built with Python. This project demonstrates the fundamentals of socket programming, multithreading for concurrent client handling, and the implementation of a basic communication protocol.

---

## About The Project

The goal of this project was to learn the core concepts of network programming in Python. It establishes a client-server architecture where a central server can accept connections from multiple clients simultaneously. Each client can send messages, which are then broadcasted by the server to its console.

This project was built from scratch to gain a deep understanding of:
*   The TCP/IP communication flow.
*   Handling multiple connections without blocking the main server.
*   Creating a simple but reliable messaging protocol.

---

## Features

*   **Client-Server Architecture:** A robust server that listens for and accepts client connections.
*   **Multi-Client Support:** Utilizes Python's `threading` module to handle each client in a separate thread, allowing for simultaneous conversations.
*   **Custom Protocol:** Implements a fixed-length header system to ensure complete and accurate message delivery between the client and server.
*   **Graceful Disconnect:** Clients can cleanly disconnect from the server by sending a specific command (`!Disconnect`).
*   **Error Handling:** Includes `try...except` blocks to manage common network errors like sudden client disconnections, ensuring server stability.

---

## Technologies Used

*   [Python 3](https://www.python.org/)
*   [`socket`](https://docs.python.org/3/library/socket.html) - Python's built-in low-level networking module.
*   [`threading`](https://docs.python.org/3/library/threading.html) - For handling concurrent client connections.

---

## How To Run

You will need two or more terminal windows to run the server and the clients.

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/YOUR_USERNAME/python-socket-chat.git
    cd python-socket-chat
    ```

2.  **Start the server:**
    Open a terminal window and run the server script. It will start listening for connections.
    ```sh
    python server.py
    ```

3.  **Start a client:**
    Open a *new* terminal window and run the client script.
    ```sh
    python client.py
    ```

4.  **Connect more clients:**
    You can open additional terminal windows and run `client.py` in each to see the multi-client functionality in action.

---

## What I Learned

Building this project provided hands-on experience with several key programming concepts:

*   **Blocking Sockets:** Understanding how `accept()` and `recv()` can pause program execution and why this necessitates a multi-threaded approach.
*   **Socket Lifecycles:** The difference between the main `server` listening socket and the individual `conn` sockets created for each client.
*   **Protocol Design:** The critical importance of defining a clear set of rules for communication (like the header system) to avoid data corruption.
*   **Concurrency vs. Parallelism:** A practical application of using threading to achieve concurrency and manage multiple I/O-bound tasks efficiently.
