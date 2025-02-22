# In setup_sockets function
def setup_sockets(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.settimeout(5.0)  # 5 second timeout
#RAJAREDDY  230001054

import socket
import threading
import time

# Store connected peers as {reported_address: (last_seen_timestamp, team_name)}
connected_peers = {}

# Add a lock for thread-safe operations on the connected_peers dictionary
peers_lock = threading.Lock()

# Function to parse the IP:PORT from a received message
def parse_peer_info(message):
    try:
        parts = message.split(' ', 2)
        if len(parts) >= 2:
            ip_port = parts[0].strip()
            ip, port_str = ip_port.split(':')
            port = int(port_str)
            team_name = parts[1].strip()
            message_content = parts[2] if len(parts) > 2 else ""
            return (ip, port), team_name, message_content
        return None, None, None
    except Exception as e:
        print(f"Error parsing peer info: {e}")
        return None, None, None

# Function to receive messages
def receive_messages(server_socket, local_ip, local_port):
    while True:
        try:
            message, addr = server_socket.recvfrom(1024)  # addr contains (Sender_IP, Sender_Port)
            decoded_msg = message.decode().strip()
            
            sender_ip, sender_port = addr  # Extract the actual sender IP and Port
            
            # Check if it's a disconnect notification
            if decoded_msg.startswith("DISCONNECT:"):
                parts = decoded_msg.split(" ", 1)
                team_info = parts[1].strip() if len(parts) > 1 else "Unknown team"
                
                with peers_lock:
                    # First check if we have this sender in our list
                    peer_to_remove = None
                    for peer_addr in list(connected_peers.keys()):
                        if peer_addr.split(":")[0] == sender_ip:
                            peer_to_remove = peer_addr
                            break
                    
                    if peer_to_remove:
                        print(f"\n[System] Peer {peer_to_remove} ({team_info}) has disconnected")
                        del connected_peers[peer_to_remove]
                    else:
                        print(f"\n[System] Unknown peer {sender_ip}:{sender_port} sent disconnect")
            else:
                # Parse the peer info from the message content
                peer_info, team_name, msg_content = parse_peer_info(decoded_msg)
                
                if peer_info and team_name:
                    # Print in the requested format
                    print(f"\nReceived from {sender_ip}:{sender_port} ({team_name}): {msg_content}")
                    
                    # Use the reported IP:PORT as the key instead of the socket address
                    reported_address = f"{peer_info[0]}:{peer_info[1]}"
                    
                    # Store the parsed IP and port in peer list with thread safety
                    with peers_lock:
                        # Record the timestamp and team name when we last heard from this peer
                        connected_peers[reported_address] = (time.time(), team_name)
                        print(f"[Debug] Added/Updated peer {reported_address} ({team_name})")
                        print(f"[Debug] Current connected peers: {len(connected_peers)}")
                else:
                    # Fallback for unparseable messages
                    print(f"\nReceived message: {decoded_msg} from {sender_ip}:{sender_port}")
                    
                    # Fallback to using the actual sender info if parsing fails
                    with peers_lock:
                        fallback_addr = f"{sender_ip}:{sender_port}"
                        connected_peers[fallback_addr] = (time.time(), "Unknown Team")
                        print(f"[Debug] Added/Updated peer {fallback_addr} (fallback)")
                
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Function to send messages to specific peer
def send_message(client_socket, team_name, target_ip, target_port, local_ip, local_port, message=None):
    if message is None:
        msg = input("\nEnter your message (type 'exit' to stop sending): ")
        if msg.lower() == 'exit':
            return False
    else:
        msg = message
    
    # Ensure target_port is an integer
    if isinstance(target_port, str):
        target_port = int(target_port)
    
    # Message format: "<IP:PORT> <Team_Name> <Message>"
    formatted_message = f"{local_ip}:{local_port} {team_name} {msg}"
    
    try:
        client_socket.sendto(formatted_message.encode(), (target_ip, target_port))
        print(f"[Sent] Message to {target_ip}:{target_port}: {msg}")
        return True
    except Exception as e:
        print(f"[Error] Failed to send message to {target_ip}:{target_port}: {e}")
        return False

# Function to send messages in a loop
def send_messages(client_socket, team_name, target_ip, target_port, local_ip, local_port):
    while True:
        if not send_message(client_socket, team_name, target_ip, target_port, local_ip, local_port):
            break

# Function to send direct message to a connected peer
def direct_message_to_peer(client_socket, team_name, local_ip, local_port):
    with peers_lock:
        if not connected_peers:
            print("\n[System] No connected peers available to message.")
            return
        
        # Display the list of connected peers with numbers
        peers_list = list(connected_peers.keys())
        print("\nConnected Peers:")
        for i, peer_addr in enumerate(peers_list, 1):
            last_seen, peer_team = connected_peers[peer_addr]
            time_diff = time.time() - last_seen
            print(f"{i}. {peer_addr} ({peer_team}) - Last active: {time_diff:.1f} seconds ago")
    
    # Let user select a peer by number
    try:
        choice = int(input("\nEnter the number of the peer you want to message (0 to cancel): "))
        if choice == 0:
            return
        
        if 1 <= choice <= len(peers_list):
            selected_peer = peers_list[choice-1]
            ip, port_str = selected_peer.split(":")
            port = int(port_str)
            
            # Get peer's team name
            with peers_lock:
                _, peer_team = connected_peers.get(selected_peer, (0, "Unknown Team"))
            
            print(f"\n[System] Starting conversation with {selected_peer} ({peer_team})")
            # Fix: Use the extracted IP and port to send messages
            send_messages(client_socket, team_name, ip, port, local_ip, local_port)
        else:
            print("\n[Error] Invalid selection.")
    except ValueError:
        print("\n[Error] Please enter a valid number.")

# Function to broadcast a message to all connected peers
def broadcast_message(client_socket, team_name, local_ip, local_port):
    with peers_lock:
        if not connected_peers:
            print("\n[System] No connected peers to broadcast to.")
            return
        
        # Make a copy of the peers to avoid modifying during iteration
        peers_copy = list(connected_peers.keys())
    
    msg = input("\nEnter your broadcast message: ")
    if not msg:
        print("[Error] Empty message not sent")
        return
        
    print(f"\n[System] Broadcasting to {len(peers_copy)} peers")
    sent_count = 0
    for peer_addr in peers_copy:
        try:
            ip, port_str = peer_addr.split(":")
            port = int(port_str)
            if send_message(client_socket, team_name, ip, port, local_ip, local_port, msg):
                sent_count += 1
        except Exception as e:
            print(f"[Error] Failed to broadcast to {peer_addr}: {e}")
    
    print(f"[System] Message broadcast to {sent_count}/{len(peers_copy)} peers")

# Function to send disconnect notification to all peers
def send_disconnect_notification(client_socket, team_name, local_ip, local_port):
    with peers_lock:
        if not connected_peers:
            return
        
        # Make a copy of the peers to avoid modifying during iteration
        peers_copy = list(connected_peers.keys())
    
    disconnect_msg = f"DISCONNECT: {team_name} has left the chat"
    
    for peer_addr in peers_copy:
        ip, port_str = peer_addr.split(":")
        port = int(port_str)
        try:
            client_socket.sendto(disconnect_msg.encode(), (ip, port))
            print(f"[System] Disconnect notification sent to {ip}:{port}")
        except Exception as e:
            print(f"[Error] Failed to send disconnect notification to {ip}:{port}: {e}")

# Function to display connected peers
def show_connected_peers():
    with peers_lock:
        print("\nConnected Peers:")
        if not connected_peers:
            print("No connected peers.")
        else:
            current_time = time.time()
            print(f"Total connected peers: {len(connected_peers)}")
            for i, peer_addr in enumerate(connected_peers, 1):
                last_seen, team_name = connected_peers[peer_addr]
                time_diff = current_time - last_seen
                print(f"{i}. {peer_addr} ({team_name}) - Last active: {time_diff:.1f} seconds ago")

# Function to connect to active peers
def connect_to_active_peers(client_socket, team_name, local_ip, local_port):
    with peers_lock:
        if not connected_peers:
            print("\n[System] No connected peers to connect to.")
            return
        
        peers_copy = list(connected_peers.keys())
    
    connection_msg = "CONNECTION_REQUEST"
    success_count = 0
    
    print(f"\n[System] Connecting to {len(peers_copy)} active peers")
    for peer_addr in peers_copy:
        try:
            ip, port_str = peer_addr.split(":")
            port = int(port_str)
            if send_message(client_socket, team_name, ip, port, local_ip, local_port, connection_msg):
                success_count += 1
                print(f"[System] Connection request sent to {ip}:{port}")
        except Exception as e:
            print(f"[Error] Failed to connect to {peer_addr}: {e}")
            
    print(f"[System] Successfully connected to {success_count}/{len(peers_copy)} peers")

# Function to send mandatory messages to specified IP addresses
def send_mandatory_messages(client_socket, team_name, local_ip, local_port):
    mandatory_peers = [
        ("10.206.4.122", 1255),
        ("10.206.5.228", 6555)
    ]
    
    # Format the mandatory message as teamname+Hello
    mandatory_message = f"{team_name} Hello"
    success_count = 0
    failed_peers = []
    
    for ip, port in mandatory_peers:
        print(f"\n[System] Attempting to send mandatory message to {ip}:{port}")
        try:
            # Message format: "<IP:PORT> <Team_Name> <Message>"
            formatted_message = f"{local_ip}:{local_port} {team_name} {mandatory_message}"
            
            # Try to send the message
            client_socket.sendto(formatted_message.encode(), (ip, port))
            
            print(f"[Sent] Message to {ip}:{port}: {mandatory_message}")
            success_count += 1
            
        except socket.error as e:
            print(f"[Failed] Could not send message to mandatory peer {ip}:{port}: {e}")
            failed_peers.append((ip, port))
        except Exception as e:
            print(f"[Error] Unknown error when connecting to mandatory peer {ip}:{port}: {e}")
            failed_peers.append((ip, port))
    
    # Report results after all attempts
    if success_count == len(mandatory_peers):
        print(f"\n[Success] Successfully sent messages to all {len(mandatory_peers)} mandatory peers.")
    else:
        print(f"\n[Warning] Could only send messages to {success_count}/{len(mandatory_peers)} mandatory peers.")
        for ip, port in failed_peers:
            print(f"  - Failed to send message to {ip}:{port}")

# Function to get local IP address
def get_local_ip():
    try:
        # This is a common trick to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        # Fallback if the above method fails
        return socket.gethostbyname(socket.gethostname())

# Function to clean up inactive peers
def cleanup_inactive_peers():
    while True:
        time.sleep(60)  # Check every minute
        current_time = time.time()
        with peers_lock:
            inactive_peers = []
            for peer_addr, (last_seen, _) in list(connected_peers.items()):
                if current_time - last_seen > 600:  # 10 minutes timeout
                    inactive_peers.append(peer_addr)
            
            for peer_addr in inactive_peers:
                print(f"\n[System] Removing inactive peer: {peer_addr}")
                del connected_peers[peer_addr]

# Setup UDP socket with a fixed port for receiving, and dynamic port for sending
def setup_sockets(port):
    # Server socket to receive messages
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("0.0.0.0", port))
    print(f"[System] Server socket bound to 0.0.0.0:{port}")
    
    # Client socket to send messages - no need to bind to a specific port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    return server_socket, client_socket

# Function to ping a specific peer to test connectivity
def ping_peer(client_socket, team_name, local_ip, local_port):
    # Let user select a peer or enter a new address
    option = input("\nPing options:\n1. Ping connected peer\n2. Ping new address\nChoose option: ")
    
    if option == "1":
        with peers_lock:
            if not connected_peers:
                print("\n[System] No connected peers available to ping.")
                return
            
            # Display the list of connected peers with numbers
            peers_list = list(connected_peers.keys())
            print("\nConnected Peers:")
            for i, peer_addr in enumerate(peers_list, 1):
                last_seen, peer_team = connected_peers[peer_addr]
                time_diff = time.time() - last_seen
                print(f"{i}. {peer_addr} ({peer_team}) - Last active: {time_diff:.1f} seconds ago")
        
        # Let user select a peer by number
        try:
            choice = int(input("\nEnter the number of the peer you want to ping (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(peers_list):
                selected_peer = peers_list[choice-1]
                target_ip, port_str = selected_peer.split(":")
                target_port = int(port_str)
            else:
                print("\n[Error] Invalid selection.")
                return
        except ValueError:
            print("\n[Error] Please enter a valid number.")
            return
    else:
        target_ip = input("Enter IP address to ping: ")
        try:
            target_port = int(input("Enter port number to ping: "))
        except ValueError:
            print("[Error] Invalid port number")
            return
    
    # Send ping message
    ping_msg = "PING"
    print(f"\n[System] Pinging {target_ip}:{target_port}...")
    start_time = time.time()
    
    try:
        # Message format: "<IP:PORT> <Team_Name> <Message>"
        formatted_message = f"{local_ip}:{local_port} {team_name} {ping_msg}"
        client_socket.sendto(formatted_message.encode(), (target_ip, target_port))
        print(f"[Sent] Ping to {target_ip}:{target_port}")
        print(f"[Debug] Raw message sent: {formatted_message}")
        
        # Successfully sent ping
        end_time = time.time()
        print(f"[Success] Ping sent in {(end_time - start_time) * 1000:.2f}ms")
    except Exception as e:
        print(f"[Error] Failed to ping {target_ip}:{target_port}: {e}")

# Main function
def main():
    team_name = input("Enter your team name: ")
    try:
        port = int(input("Enter your port number: "))
    except ValueError:
        print("[Error] Invalid port number, using default port 5000")
        port = 5000
    
    # Get local IP address
    local_ip = get_local_ip()
    print(f"[System] Your IP address: {local_ip}")

    # Set up UDP sockets
    server_socket, client_socket = setup_sockets(port)
    print(f"[System] Listening on port {port}")

    # Start receiving messages in a separate thread
    recv_thread = threading.Thread(target=receive_messages, args=(server_socket, local_ip, port))
    recv_thread.daemon = True
    recv_thread.start()
    
    # Start cleanup thread for inactive peers
    cleanup_thread = threading.Thread(target=cleanup_inactive_peers)
    cleanup_thread.daemon = True
    cleanup_thread.start()
    
    # Send mandatory messages after a short delay to ensure server is ready
    time.sleep(1)
    print("\n[System] Sending mandatory messages to required peers...")
    send_mandatory_messages(client_socket, team_name, local_ip, port)

    while True:
        print("\n***** Menu *****")
        print("1. Send Message (Manual IP Entry)")
        print("2. Direct Message to Connected Peer")
        print("3. Query Connected Peers")
        print("4. Broadcast Message to All Peers")
        print("5. Connect to Active Peers")
        print("6. Resend Mandatory Messages") 
        print("7. Ping Peer (Test Connectivity)")
        print("0. Quit")

        choice = input("Enter choice: ")

        if choice == "1":
            target_ip = input("Enter recipient's IP address: ")
            try:
                target_port = int(input("Enter recipient's port number: "))
                send_messages(client_socket, team_name, target_ip, target_port, local_ip, port)
            except ValueError:
                print("[Error] Invalid port number")
            
        elif choice == "2":
            direct_message_to_peer(client_socket, team_name, local_ip, port)

        elif choice == "3":
            show_connected_peers()
            
        elif choice == "4":
            broadcast_message(client_socket, team_name, local_ip, port)
            
        elif choice == "5":
            connect_to_active_peers(client_socket, team_name, local_ip, port)
            
        elif choice == "6":
            print("\n[System] Resending mandatory messages...")
            send_mandatory_messages(client_socket, team_name, local_ip, port)
            
        elif choice == "7":
            ping_peer(client_socket, team_name, local_ip, port)

        elif choice == "0":
            print("Sending disconnect notifications...")
            send_disconnect_notification(client_socket, team_name, local_ip, port)
            print("Exiting program....")
            break
        else:
            print("Invalid choice! Please enter again.")

if __name__ == "__main__":
    main()