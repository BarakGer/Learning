import socket

def main():
    """
    writing a client for an existing server in "networks.cyber.org.il"
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.sendto(b'Barak', ('54.213.229.251', 8821))
    (data, remote_address) = my_socket.recvfrom(1024)
    print('the server sent back: ' + data.decode('utf-8'))
    my_socket.close()


if __name__ == '__main__':
    main()