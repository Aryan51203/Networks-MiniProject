#!/bin/bash

# Start the server in the background (both IPv4 and IPv6)
echo "Starting server..."
python3 server.py &
SERVER_PID=$!
echo "Server started with PID $SERVER_PID"

# Wait a few seconds to ensure server is running
sleep 3

# Start the client (with Tkinter GUI)
echo "Starting client GUI..."
python3 client.py

# When the client GUI is closed, kill the server process
echo "Stopping server..."
kill $SERVER_PID
echo "Server stopped."

# Exit
exit 0
