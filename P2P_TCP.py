#TEAM CRYPTOSPHERE
#SUDHEENDRA 230001076
#VIKAS      230002023
#RAJAREDDY  230001054

import socket
import threading
import time
from datetime import datetime
import sys

# Constants
INACTIVITY_TIMEOUT_SECONDS = 600  # 10 minutes
CONNECTION_TIMEOUT_SECONDS = 5
SOCKET_BUFFER_SIZE = 1024
SERVER_BACKLOG = 5
SERVER_CHECK_INTERVAL = 1
DNS_SERVICE_IP = "8.8.8.8"
DNS_SERVICE_PORT = 53
PORT_RANGE_MIN = 1024
PORT_RANGE_MAX = 65535

# Network message constants
MSG_DISCONNECT = "DISCONNECT"
MSG_CONNECTION_REQUEST = "CONNECTION_REQUEST"
MSG_END_MARKER = "<end>"
MSG_EXIT_COMMAND = "exit"

# Global state
network_peers = {}
network_peers_lock = threading.Lock()
user_team_identifier = ""
server_socket_global = None
is_application_running = True

# Optional peer configuration
mandatory_network_peers = [
    ("10.206.4.122", 1255),
    ("10.206.5.228", 6555)
]

class NetworkPeer:
    """Represents a peer in the network with connection details and status"""
    def __init__(self, ip_address, port_number):
        self.ip_address = ip_address
        self.port_number = port_number
        self.last_activity_timestamp = time.time()

def monitor_peer_activity():
    """Monitor and remove inactive peers based on timeout threshold"""
    while is_application_running:
        time.sleep(SERVER_CHECK_INTERVAL)
        with network_peers_lock:
            current_time = time.time()
            inactive_peer_addresses = []
            
            for peer_address, peer in list(network_peers.items()):
                if current_time - peer.last_activity_timestamp > INACTIVITY_TIMEOUT_SECONDS:
                    print(f"Removing inactive peer: {peer_address}")
                    inactive_peer_addresses.append(peer_address)
            
            for peer_address in inactive_peer_addresses:
                network_peers.pop(peer_address, None)

def get_local_network_address():
    """Determine local network address through DNS service connection"""
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect((DNS_SERVICE_IP, DNS_SERVICE_PORT))
        local_address = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_address
    except Exception:
        return "Unknown"

def register_peer(ip_address, port_number):
    """Register or update peer in the network"""
    with network_peers_lock:
        peer_address = f"{ip_address}:{port_number}"
        if peer_address not in network_peers:
            network_peers[peer_address] = NetworkPeer(ip_address, port_number)
            print(f"\n[System] New peer connected: {peer_address}")
        else:
            network_peers[peer_address].last_activity_timestamp = time.time()

def display_active_peers():
    """Display list of all currently active peers with last seen timestamps and return the list"""
    peer_list = []
    with network_peers_lock:
        print("\n╔═══════════════════ Active Network Peers ══════════════════╗")
        if not network_peers:
            print("║              No active peers connected                    ║")
        else:
            for i, peer_address in enumerate(network_peers, 1):
                peer = network_peers[peer_address]
                last_seen = datetime.fromtimestamp(peer.last_activity_timestamp).strftime("%H:%M:%S")
                print(f"║ {i}. {peer_address:<33} Last seen: {last_seen}  ║")
                peer_list.append(peer_address)
        print("╚═══════════════════════════════════════════════════════════╝")
    return peer_list

def send_message_to_friend():
    """Send a message to a specific connected peer"""
    peer_list = display_active_peers()
    if not peer_list:
        print("\n[Error] No peers available to message")
        return

    try:
        choice = int(input("\nEnter peer number (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(peer_list):
            peer_address = peer_list[choice - 1]
            with network_peers_lock:
                if peer_address in network_peers:
                    peer = network_peers[peer_address]
                    message = input("\nEnter your message: ")
                    transmit_message(message, peer.ip_address, peer.port_number, int(peer_address.split(':')[1]))
                    print(f"\n[Success] Message sent to {peer_address}")
                else:
                    print("\n[Error] Selected peer is no longer connected")
        else:
            print("\n[Error] Invalid selection")
    except ValueError:
        print("\n[Error] Please enter a valid number")

def remove_specific_peer():
    """Remove a specific peer from the network"""
    peer_list = display_active_peers()
    if not peer_list:
        print("\n[Error] No peers to remove")
        return

    try:
        choice = int(input("\nEnter peer number to remove (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(peer_list):
            peer_address = peer_list[choice - 1]
            with network_peers_lock:
                if peer_address in network_peers:
                    peer = network_peers[peer_address]
                    # Send disconnect message to the peer
                    transmit_message(MSG_DISCONNECT, peer.ip_address, peer.port_number, int(peer_address.split(':')[1]))
                    network_peers.pop(peer_address)
                    print(f"\n[Success] Removed peer: {peer_address}")
                else:
                    print("\n[Error] Selected peer is no longer connected")
        else:
            print("\n[Error] Invalid selection")
    except ValueError:
        print("\n[Error] Please enter a valid number")

def deregister_peer(peer_address):
    """Remove peer from the network"""
    with network_peers_lock:
        if peer_address in network_peers:
            network_peers.pop(peer_address)
            print("\n╔═════════════ Peer Disconnected ═════════════╗")
            print(f"║ {peer_address:<41} ║")
            print("╚═════════════════════════════════════════════╝")

def format_chat_message(team, content):
    """Format the chat message for better readability"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    return f"[{timestamp}] Team {team}: {content}"

def transmit_message(message_content, recipient_ip, recipient_port, sender_port):
    """Transmit message to specified peer"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(CONNECTION_TIMEOUT_SECONDS)
        client_socket.connect((recipient_ip, recipient_port))
        
        # Format message based on type
        local_ip = get_local_network_address()
        if message_content == MSG_DISCONNECT:
            formatted_message = f"<{local_ip}:{sender_port}> {MSG_DISCONNECT}"
        else:
            formatted_message = (
                f"<{local_ip}:{sender_port}> @ <{user_team_identifier}>\n"
                f"{message_content}\n{MSG_END_MARKER}"
            )
        
        client_socket.sendall(formatted_message.encode())
        print(f"\n[Success] Message sent to {recipient_ip}:{recipient_port}")
    except (socket.timeout, ConnectionRefusedError, OSError) as error:
        print(f"\n[Error] Failed to send message to {recipient_ip}:{recipient_port} - {str(error)}")
        peer_address = f"{recipient_ip}:{recipient_port}"
        deregister_peer(peer_address)
        return False
    finally:
        client_socket.close()
    return True

def continuous_messaging_session(recipient_ip, recipient_port, local_port):
    """Handle continuous messaging session with a peer"""
    print("\n╔════════ Starting Chat Session ═══════════════╗")
    print(f"║ Connected to: {recipient_ip}:{recipient_port:<16} ")
    print(f"║ Type '{MSG_EXIT_COMMAND}' to return to main menu  ")
    print("╚═══════════════════════════════════════════════╝")

    while True:
        try:
            message = input("\nYou: ")
            if message.lower() == MSG_EXIT_COMMAND:
                print("\n[System] Ending chat session...")
                break
            
            success = transmit_message(message, recipient_ip, recipient_port, local_port)
            if not success:
                print("[System] Failed to deliver message. Ending chat session...")
                break
        except KeyboardInterrupt:
            print("\n[System] Chat session interrupted")
            break
def initialize_server(port_number):
    """Initialize and run server for incoming connections"""
    global server_socket_global
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', port_number))
        server_socket.listen(SERVER_BACKLOG)
        server_socket.settimeout(SERVER_CHECK_INTERVAL)
        server_socket_global = server_socket
        
        print(f"[System] Server running on port {port_number}")
        
        while is_application_running:
            try:
                client_socket, client_address = server_socket.accept()
                client_ip, client_port = client_address
                
                # Process incoming message
                received_data = client_socket.recv(SOCKET_BUFFER_SIZE).decode()
                
                # Extract sender port from message header
                sender_port = client_port
                if received_data and received_data.startswith('<'):
                    header_end = received_data.find('>')
                    if header_end != -1:
                        port_start = received_data.find(':', 1)
                        if port_start != -1 and port_start < header_end:
                            try:
                                sender_port = int(received_data[port_start+1:header_end])
                            except ValueError:
                                pass
                
                register_peer(client_ip, sender_port)
                
                # Parse and display message
                if received_data:
                    # Handle disconnect message
                    if MSG_DISCONNECT in received_data:
                        peer_address = f"{client_ip}:{sender_port}"
                        deregister_peer(peer_address)
                    else:
                        # Parse message components
                        team_start = received_data.find("@ <") + 3
                        team_end = received_data.find(">", team_start)
                        message_start = received_data.find("\n", team_end) + 1
                        message_end = received_data.find("\n<end>")
                        
                        if all(x != -1 for x in [team_start, team_end, message_start, message_end]):
                            team = received_data[team_start:team_end]
                            message = received_data[message_start:message_end]
                            
                            # Display formatted message
                            print("\n╔════════════════ Message Received ════════════════╗")
                            print(f"║ From: {client_ip}:{sender_port:<31} ")
                            print(f"║ Team: {team:<37} ")
                            print(f"║ Message: {message:<34} ")
                            print("╚══════════════════════════════════════════════════╝")
                            
                            # If in chat mode, show prompt again
                            print("You: ", end='', flush=True)
                
                client_socket.close()
            
            except socket.timeout:
                continue
            except Exception as error:
                if is_application_running:
                    print(f"\n[Error] Server error: {str(error)}")
                continue
    
    except Exception as error:
        print(f"\n[Error] Server initialization failed: {str(error)}")
    finally:
        if server_socket:
            server_socket.close()

def main():
    """Main application entry point"""
    global user_team_identifier, is_application_running
    
    try:
        print("\n╔══════ Peer Network Application ═══════╗")
        user_team_identifier = input("║ Enter your Team name: ")
        while True:
            try:
                local_port = int(input("║ Enter your port number: "))
                if PORT_RANGE_MIN <= local_port <= PORT_RANGE_MAX:
                    break
                print("║ [Error] Invalid port. Use range 1024-65535 ║")
            except ValueError:
                print("║ [Error] Please enter a valid number   ║")
        print("╚═══════════════════════════════════════╝")
        
        print(f"\n[System] Local IP address: {get_local_network_address()}")
        
        # Initialize network threads
        server_thread = threading.Thread(target=initialize_server, args=(local_port,))
        monitoring_thread = threading.Thread(target=monitor_peer_activity)
        
        server_thread.daemon = True
        monitoring_thread.daemon = True
        
        server_thread.start()
        monitoring_thread.start()
        
        for peer_ip, peer_port in mandatory_network_peers:
            threading.Thread(target=transmit_message, args=(f"{user_team_identifier}: Hello", peer_ip, peer_port, local_port)).start()
        
        # Main application loop
        while True:
            time.sleep(SERVER_CHECK_INTERVAL)
            
            print("\n╔═════════ Network Control Panel ══════════╗")
            print("║ 1. Start messaging session               ║")
            print("║ 2. View active peers                     ║")
            print("║ 3. Connect to peers                      ║")
            print("║ 4. Broadcast message                     ║")
            print("║ 5. Send message to friend                ║")
            print("║ 6. Remove connected peer                 ║")
            print("║ 0. Quit Application                      ║")
            print("╚══════════════════════════════════════════╝")
            
            user_choice = input("Select option: ")
            
            try:
                if user_choice == "1":
                    target_ip = input("Enter recipient IP: ")
                    target_port = int(input("Enter recipient port: "))
                    continuous_messaging_session(target_ip, target_port, local_port)
                
                elif user_choice == "2":
                    display_active_peers()
                
                elif user_choice == "3":
                    with network_peers_lock:
                        active_peers = list(network_peers.values())
                    
                    for peer in active_peers:
                        threading.Thread(
                            target=transmit_message,
                            args=(MSG_CONNECTION_REQUEST, peer.ip_address, peer.port_number, local_port)
                        ).start()
                    print("\n[Success] Connection requests sent to all active peers")
                
                elif user_choice == "4":
                    broadcast_message = input("Enter broadcast message: ")
                    with network_peers_lock:
                        active_peers = list(network_peers.values())
                    
                    for peer in active_peers:
                        threading.Thread(
                            target=transmit_message,
                            args=(broadcast_message, peer.ip_address, peer.port_number, local_port)
                        ).start()
                    print("\n[Success] Broadcast message sent to all peers")

                elif user_choice == "5":
                    send_message_to_friend()

                elif user_choice == "6":
                    remove_specific_peer()
                
                elif user_choice == "0":
                    print("\n[System] Initiating shutdown sequence...")
                    with network_peers_lock:
                        active_peers = list(network_peers.values())
                    
                    for peer in active_peers:
                        threading.Thread(
                            target=transmit_message,
                            args=(MSG_DISCONNECT, peer.ip_address, peer.port_number, local_port)
                        ).start()
                    
                    is_application_running = False
                    if server_socket_global:
                        server_socket_global.close()
                    break
                
                else:
                    print("\n[Error] Invalid option selected")
            
            except ValueError:
                print("\n[Error] Invalid input. Please check your values")
            except Exception as error:
                print(f"\n[Error] Operation failed: {str(error)}")
        
        # Allow time for disconnect messages
        time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n\n[System] Application interrupted")
    finally:
        is_application_running = False
        if server_socket_global:
            server_socket_global.close()
        print("[System] Shutdown complete")
        sys.exit(0)

if __name__ == "__main__":
    main()