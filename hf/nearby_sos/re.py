import socket

def send_udp_alert(message, server_ip='255.255.255.255', port=5005):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Send message to the broadcast address
    client_socket.sendto(message.encode(), (server_ip, port))
    print(f"Sent alert: {message}")

if __name__ == '__main__':
    # Example usage
    alert_message = "Emergency Alert! Please respond!"
    send_udp_alert(alert_message)
