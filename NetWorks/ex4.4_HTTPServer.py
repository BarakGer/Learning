# TO DO: import modules
import socket
import os
import io

# TO DO: set constants
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 0.2 * 60
HEADER_END = "\r\n\r\n"
REQUEST_END = HEADER_END #we have only GET requests so there is no data part after headers
RECV_BUFFER = 1024
DEFAULT_URL = '\\index.html'
HTTP_VERSION = 'HTTP/1.0 '
REDIRECTION_DICTIONARY = {os.curdir + '\\webroot' + '\\js\\box.js': 'http://127.0.0.1/js2/box.js' }

def get_file_data(filename):
    """ Get data from file """
    with open(filename, 'rb') as file:
        data = file.read()
        return data



def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    if resource == '\\':
        url = os.curdir + '\\webroot' + DEFAULT_URL
    else:
        url = os.curdir + '\\webroot' + resource

    # TO DO: check if URL had been redirected, not available or other error code.
    redirected = False
    if os.path.isfile(url):
        http_response = HTTP_VERSION + '200 ok\r\n'
        data = get_file_data(url)
        http_header = 'Content-Length: ' + str(len(data))
    elif url in REDIRECTION_DICTIONARY:
        redirected = True
        http_response = HTTP_VERSION + '302 Moved Temporarily\r\n'
        http_header = 'Content-Type: text/html' '\r\nLocation: ' + REDIRECTION_DICTIONARY[url]\
                     + '\r\nRetry-After: 0.1' + '\r\nstatus: 302' + HEADER_END  # TO DO: send 302 redirection response
        data = ''
    else:  # not(os.path.isfile(url)):
        http_response = HTTP_VERSION + '404 Not Found\r\n'
        http_header = '\r\n'
        data = ''

    # TO DO: extract requested file type from URL (html, jpg etc)
    filetype = url[(url.rfind('.')+1):]
    if redirected:
        pass
    elif filetype == 'html':
        http_header += 'Content-Type: text/html\r\ncharset=utf-8' + HEADER_END  # TO DO: generate proper HTTP header
    elif filetype == 'jpg':
        http_header += 'Content-Type: image/jpeg' + HEADER_END # TO DO: generate proper jpg header
    # TO DO: handle all other headers
    elif filetype == 'js':
        http_header += 'Content-Type: text/javascript\r\ncharset=UTF-8' + HEADER_END
    elif filetype == 'css':
        http_header += 'Content-Type: text/css' + HEADER_END
    else:
        http_header += HEADER_END
    # TO DO: read the data from the file

    full_http_response = http_response + http_header + data
    client_socket.send(full_http_response)


'''
def handle_client_request(resource, client_socket):
    if resource == '\\':
        url = os.curdir + '\\webroot' + DEFAULT_URL
    else:
        url = os.curdir + '\\webroot' + resource
    http_response = get_file_data(url)
    client_socket.send(http_response)
    print 'handled request\n' \
          'sent ' + url
'''


def validate_http_request(request_with_headers):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    # TO DO: write function
    request = request_with_headers[:request_with_headers.find('\r\n')]
    splitted_request = request.split(' ')
    valid_http = False
    resource = ''
    try:
        http_version = splitted_request[2]
    except:
        valid_http =False
    if splitted_request.__len__() != 3:
        valid_http = False
    elif splitted_request[0] != 'GET':
        valid_http = False
    elif not(http_version.startswith('HTTP/')) or not(http_version[http_version.find('/')+1].isdigit()) \
            or http_version[http_version.find('/')+2] != '.' or not(http_version[http_version.find('/')+3].isdigit()):
        valid_http = False
    else:
        valid_http = True
        resource = splitted_request[1].replace('/', '\\')
    return valid_http, resource


def recieve_request(client_socket, cur_request):
    """ recieve request and do segmentation """
    print 'recieving request'
    while cur_request.find(REQUEST_END) == -1 or cur_request == '':
        cur_request += client_socket.recv(RECV_BUFFER)
    request = cur_request[:cur_request.find(REQUEST_END)]
    return request


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print 'Client connected'
    cur_request = ''
    while True:
        # TO DO: insert code that receives client request
        client_request = recieve_request(client_socket, cur_request)
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print 'Got a valid HTTP request'
            handle_client_request(resource, client_socket)
            break
        else:
            print 'Error: Not a valid HTTP request'
            break
    print 'Closing connection'
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    print "Listening for connections on port %d" % PORT

    while True:
        client_socket, client_address = server_socket.accept()
        print 'New connection received'
        client_socket.settimeout(SOCKET_TIMEOUT)
        try:
            handle_client(client_socket)
        except socket.timeout:
            print 'socket timed out'



if __name__ == "__main__":
    # Call the main handler function
    main()