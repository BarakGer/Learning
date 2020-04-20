# -*- coding: utf-8 -*-
import socket

def main():
    """
    Echo Server
    """
    server_socket = socket.socket()

    server_socket.bind(('0.0.0.0', 1729))
    server_socket.listen(1)

    (client_socket, client_address) = server_socket.accept()

    massage = client_socket.recv(1024)
    client_socket.send(massage)

    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
