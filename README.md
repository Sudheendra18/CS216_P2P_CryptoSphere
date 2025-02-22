# CryptoSphere
BLOCKCHAIN ASSIGNMENT1
# Project CRYPTOSPHERE

A robust peer-to-peer TCP networking application that enables secure communication between network peers with features like real-time messaging, peer monitoring, and broadcast capabilities.

## Project Details
- **Project Name**: CRYPTOSPHERE
- **Main File**: P2P_TCP.py
- **Version**: 1.0
- **Type**: Peer-to-Peer Network Application
- **Protocol**: TCP/IP

## Team Members
- Sudheendra (230001076)
- Vikas (230002023)
- Rajareddy (230001054)

## Table of Contents
1. [Features](#features)
2. [Technical Specifications](#technical-specifications)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Architecture](#architecture)
6. [Error Handling](#error-handling)
7. [Contributing](#contributing)
8. [License](#license)

## Features

### Core Networking Features
1. **Real-time TCP Communication**
   - Reliable TCP-based peer-to-peer messaging
   - Automatic connection management
   - Dynamic port allocation (1024-65535)
   - Configurable socket buffer size (1024 bytes)

2. **Peer Discovery and Management**
   - Automatic local IP detection via DNS service
   - Dynamic peer registration system
   - Real-time peer activity monitoring
   - Automatic inactive peer cleanup (10-minute timeout)
   - Support for mandatory network peers
   - Thread-safe peer management

3. **Messaging Capabilities**
   - Direct peer-to-peer messaging
   - Broadcast messaging to all connected peers
   - Continuous messaging sessions
   - Formatted message display with timestamps
   - Team identifier integration in messages
   - Message end markers for integrity
   - Connection request protocol
   - Disconnect notification system

### Server Features
1. **Multi-threaded Server Architecture**
   - Concurrent connection handling
   - Configurable server backlog (5 connections)
   - Server timeout handling (1-second check interval)
   - Graceful server shutdown

2. **Connection Management**
   - Connection timeout handling (5 seconds)
   - Automatic port conflict resolution
   - Socket reuse address support
   - Server backlog management

### User Interface Features
1. **Interactive Console Interface**
   - ASCII-art based menu system
   - Real-time status updates
   - Formatted message display
   - Active peer listing with timestamps
   - Error notifications and system messages

2. **Menu Options**
   - Start messaging session
   - View active peers
   - Connect to peers
   - Broadcast message
   - Send message to specific friend
   - Remove connected peer
   - Graceful application exit

## Technical Specifications

### System Requirements
- Python 3.x
- Standard library modules:
  - socket
  - threading
  - time
  - datetime
  - sys

### Network Configuration
- Default DNS Service: 8.8.8.8 (Port 53)
- Valid Port Range: 1024-65535
- Socket Buffer Size: 1024 bytes
- Server Backlog: 5 connections
- Server Check Interval: 1 second
- Inactivity Timeout: 600 seconds (10 minutes)
- Connection Timeout: 5 seconds

### Constants
```python
INACTIVITY_TIMEOUT_SECONDS = 600
CONNECTION_TIMEOUT_SECONDS = 5
SOCKET_BUFFER_SIZE = 1024
SERVER_BACKLOG = 5
SERVER_CHECK_INTERVAL = 1
```

## Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/CRYPTOSPHERE.git
cd CRYPTOSPHERE
```

2. **Verify Python Installation**
```bash
python --version  # Should be Python 3.x
```

3. **Run the Application**
```bash
python P2P_TCP.py
```

## Usage

### Starting the Application

1. Launch the application:
```bash
python P2P_TCP.py
```

2. Initial Setup:
   - Enter your Team name when prompted
   - Enter your desired port number (1024-65535)

### Main Menu Navigation

The application presents a menu with the following options:

```
╔═════════ Network Control Panel ══════════╗
║ 1. Start messaging session               ║
║ 2. View active peers                     ║
║ 3. Connect to peers                      ║
║ 4. Broadcast message                     ║
║ 5. Send message to friend                ║
║ 6. Remove connected peer                 ║
║ 0. Quit Application                      ║
╚══════════════════════════════════════════╝
```

### Feature Usage

1. **Starting a Messaging Session**
   - Select option 1
   - Enter recipient IP
   - Enter recipient port
   - Type 'exit' to end session

2. **Viewing Active Peers**
   - Select option 2
   - Displays list with connection times

3. **Connecting to Peers**
   - Select option 3
   - Automatically sends connection requests

4. **Broadcasting Messages**
   - Select option 4
   - Enter message to send to all peers

5. **Direct Messaging**
   - Select option 5
   - Choose peer from list
   - Enter message

6. **Removing Peers**
   - Select option 6
   - Select peer to remove

## Architecture

### Class Structure

1. **NetworkPeer Class**
```python
class NetworkPeer:
    def __init__(self, ip_address, port_number):
        self.ip_address = ip_address
        self.port_number = port_number
        self.last_activity_timestamp = time.time()
```

### Key Components

1. **Network Management**
   - Peer registration
   - Activity monitoring
   - Connection handling
   - Message routing

2. **Threading Model**
   - Server thread
   - Monitoring thread
   - Message handling threads

3. **Message Protocol**
   - Header format: `<IP:PORT>`
   - Team identifier: `@ <TEAM>`
   - End marker: `<end>`

## Error Handling

### Network Errors
- Connection timeouts
- Invalid peer connections
- Port binding failures
- Socket errors

### User Input Errors
- Invalid port numbers
- Incorrect IP addresses
- Invalid menu selections

### System Errors
- Resource allocation failures
- Thread management issues
- Memory management

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Specify your license here]

## Notes

- Ensure proper network connectivity before running
- Keep track of port numbers in use
- Monitor system resources for optimal performance
- Regular cleanup of inactive connections recommended

## Future Enhancements

1. **Security Features**
   - End-to-end encryption
   - Authentication system
   - Access control lists

2. **User Interface**
   - Graphical user interface
   - Web interface option
   - Mobile application support

3. **Functionality**
   - File transfer capabilities
   - Group chat features
   - Message persistence
   - Offline messaging

## Support

For support or queries, contact:
[sudheendra1808@gmail.com]
