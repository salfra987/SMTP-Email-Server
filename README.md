# SMTP-Email-Server

This project implements a simple SMTP communication system, including a client, server, and SMTP command parsing and handling.

## Files

### parse.py
This file contains functions for parsing SMTP commands. It ensures that commands are correctly formatted and processes different parts of an SMTP message.

### SMTP1.py
This file handles SMTP operations, including sending emails and parsing SMTP responses. It ensures that the correct SMTP commands are sent and processes responses from the server. This extends the work done in parse.py.

### SMTP2.py
This file handles another part of the SMTP operations, similar to SMTP1.py. It includes functions for sending emails and parsing responses, ensuring proper communication with the SMTP server. This file builds off of the work done in SMTP1.py.

### Client.py
This file contains the client-side implementation for connecting and communicating with an SMTP server. The client sends commands and handles responses from the server.

### Server.py
This file contains the server-side implementation for receiving and processing client requests. The server handles SMTP commands sent by the client and responds accordingly.

## How to Run

1. **Server**: Start the server by running `Server.py`. This will set up the SMTP server to listen for incoming client connections.

    ```bash
    python Server.py
    ```

2. **Client**: Connect to the server by running `Client.py`. This will start the SMTP client and enable it to send commands to the server.

    ```bash
    python Client.py
    ```

3. **SMTP Operations**: The `parse.py`, `SMTP1.py`, and `SMTP2.py` files will be used internally by the client and server to parse SMTP commands and responses.

## Requirements

- Python 3.x
- Standard Python libraries (e.g., `os`, `sys`)

## Features

- Basic SMTP client and server implementation
- Parsing of SMTP commands
- Handling SMTP operations (sending emails, parsing responses)

## License

This project is licensed under the MIT License.
