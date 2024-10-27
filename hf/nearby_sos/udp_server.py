import socket

def start_udp_server(port=5005):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))  # Bind to all interfaces on the specified port
    print(f"UDP server is listening on port {port}...")

    while True:
        message, client_address = server_socket.recvfrom(1024)  # Buffer size of 1024 bytes
        print(f"Received alert: {message.decode()} from {client_address}")
        # Here you can implement additional logic (e.g., logging, processing alerts)

if __name__ == '__main__':
    start_udp_server()
