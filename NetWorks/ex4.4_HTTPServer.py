# import modules
import socket
import BaseHTTPServer
import SimpleHTTPServer
import SocketServer

# set constants
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT =0.25 * 60
REQUEST_END = "\\r\\n\\r\\n" #we have only GET requests so there is no data part after headers

def is_valid_HTTP_request(HTTP_request):
    """ check if the request is valid; if it's valid return requested resource """
    is_valid = HTTP_request.parse_request()
    if is_valid and HTTP_request.command == 'GET':
        requested_resource = HTTP_request.path
    else:
        requested_resource = None
    return (is_valid and HTTP_request.command == 'GET'), requested_resource

def recieve_request(client_socket, cur_request):
    """ recieve request and do segmentation """
    print 'recieving request'
    #while cur_request.find(REQUEST_END) == -1:
    #    cur_request += client_socket.recv(1024)
    cur_request = client_socket.recv(1024)
    request = cur_request[:(cur_request.find(REQUEST_END) + len(REQUEST_END))]
    start_of_next_request = cur_request[cur_request.find(REQUEST_END) + len(REQUEST_END):]
    print 'recieved: %s' % request
    return request, start_of_next_request



def handle_client(client_socket, client_address):
    """ handle a client connection - verify it is a legal HTTP request and handle it accordingly """
    print 'start handling'
    HTTP_request = SimpleHTTPServer.SimpleHTTPRequestHandler(client_socket, client_address, SimpleHTTPServer)
    cur_request = ''
    while True:
        print 'start recieving'
        HTTP_request.raw_requestline, start_of_next_request = recieve_request(client_socket, cur_request)

        is_valid, requested_resource = is_valid_HTTP_request(HTTP_request)
        if is_valid:
            return requested_resource
        else:
            print 'Error:    the request is not valid'
            break
        cur_request = start_of_next_request
    print 'closing connection'
    client_socket.close()


def main():
    """ Open a socket and loop forever while waiting for clients """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    print "Listening for connections on port %d" % PORT

    while True:
        client_socket, client_address = server_socket.accept()
        print 'New connection received'
        #cur_request = ''
        #request, start_of_next_request = recieve_request(client_socket, cur_request)
        client_socket.settimeout(SOCKET_TIMEOUT)
        try:
            handle_client(client_socket, client_address)
        except socket.timeout:
            print 'socket timed out'


if __name__ == "__main__":
    main()