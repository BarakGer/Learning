import socket


def main():
    """
    writing a client for an existing echo server
    """
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    my_socket.sendto(b'Echo', ("127.0.0.1", 1729))
    (data, remote_address) = my_socket.recvfrom(1024)
    print('Server sent back: ' + data.decode('utf-8'))
    my_socket.close()


if __name__ == '__main__':
    main()