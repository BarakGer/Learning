import socket

''' UDP Echo Server '''

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('0.0.0.0', 1729))
(client_data, client_address) = server_socket.recvfrom(1024)
server_socket.sendto(client_data, client_address)
server_socket.close()
