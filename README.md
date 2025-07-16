# Local Chat Messenger

![Live demo](assets/demo.gif)
*The demo shows client-server communication with timestamp logging and various message types.*

A UDP-based chat application built with Python that demonstrates socket programming concepts.

## Features

- UDP socket communication using UNIX domain sockets
- Real-time message exchange between client and server
- Server generates fake responses using the Faker library
- Interactive client with timestamp logging
- Graceful error handling and timeout management

## Prerequisites

- Python 3.7+
- pip 

## Installation
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (macOS/Linux)
4. Install dependencies: `pip install -r requirements.txt`

## Usage 
1. Start the server: `python udp-server.py`
2. In another terminal, start the client: `python udp-client.py`
3. Type messages and see the server's fake responses!
4. Type 'quit' to exit the client

## Commands
- Send "name" to get a fake name
- Send "address" to get a fake address
- Send "email" to get a fake email
- Send "text" to get a fake text
- Any other message gets a random sentence

## Cleanup
- To stop the server, press `Ctrl+C`
- To stop the client, type 'quit'
- The server will automatically clean up the socket file when it exits

## Learning Objectives
This project demonstrates:
- UDP vs TCP socket programming
- UNIX domain sockets
- Error handling in networking programming
- Using external libraries (Faker)
- Interactive command-line applications

## Version
Current version: 1.0.0