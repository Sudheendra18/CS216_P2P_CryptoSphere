# CryptoSphere
# Project  Peer-to-Peer Chat Application 
### Using TCP

A robust peer-to-peer TCP networking application that enables secure communication between network peers with features like real-time messaging, peer monitoring, and broadcast capabilities.

## Project Details
- **Team Name**: CRYPTOSPHERE
- **Main File**: P2P_TCP.py
- **Type**: Peer-to-Peer Network Application
- **Protocol**: TCP/IP

## Team Members
- Sudheendra (230001076)
- Vikas (230002023)
- Rajareddy (230001054)


## Installation

1. **Clone the Repository**
```bash
git clone https://github.com/Sudheendra18/CS216_P2P_CryptoSphere.git
cd CS216_P2P_CryptoSphere
```

2. **Run the Application**
```bash
python P2P_TCP.py
```

3. **Verify Python Installation**
```bash
python --version  # Should be Python 3.x
```

## Features

### Core Networking Features
1. **Real-time TCP Communication**
   - Reliable TCP-based peer-to-peer messaging
   - Automatic connection management
   - Configurable socket buffer size (1024 bytes)

2. **Peer Discovery and Management**
   - Automatic local IP detection via DNS service
   - Dynamic peer registration system
   - Real-time peer activity monitoring
   - Automatic inactive peer cleanup (10-minute timeout)

### Server Features
1. **Multi-threaded Server Architecture**
   - Concurrent connection handling
   - Configurable server backlog (5 connections)
   - Server timeout handling (1-second check interval)

2. **Connection Management**
   - Automatic port conflict resolution
   - Socket reuse address support
   - Server backlog management

## Technical Specifications

### System Requirements
- Python 3.x
- Standard library modules:
  - socket
  - threading

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

## DEMO
https://github.com/user-attachments/assets/7ea966f6-928b-4354-aaee-8a47060fb92d

## Support

For support or queries, contact:
[sudheendra1808@gmail.com]
