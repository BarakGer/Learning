import socket

''' basic UDP server '''

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('0.0.0.0', 8821))
(client_name, client_address) = server_socket.recvfrom(1024)
server_socket.sendto('Hello ' + client_name, client_address)
server_socket.close()