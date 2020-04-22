import socket
import os
import io

IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 0.18 * 60
HEADER_END = "\r\n\r\n"
REQUEST_END = HEADER_END #we have only GET requests so there is no data part after headers
RECV_BUFFER = 1024
DEFAULT_URL = '\\index.html'
HTTP_VERSION = 'HTTP/1.0 '
REDIRECTION_DICTIONARY = {os.curdir + '\\webroot' + '\\js\\box.js': 'http://127.0.0.1/js2/box.js'}
SPECIAL_DICTIONARY = {os.curdir + '\\webroot' + '\\calculate-next': 'next_num',
                      os.curdir + '\\webroot' + '\\calculate-area': 'area'}

def calaculate_area(parameters):
    parameter_list = parameters.split('&')
    param1 = float(parameter_list[0][parameter_list[0].find('=')+1:])
    param2 = float(parameter_list[1][parameter_list[1].find('=')+1:])
    return str(param1*param2/2)


def get_next_num(parameter):
    num = int(parameter[parameter.find('=')+1:])
    return str(num+1)


def get_file_data(filename):
    """ Get data from file """
    with open(filename, 'rb') as file:
        data = file.read()
        return data
     # SHLAIN: What do you return if can't open ?



def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    splitted_resource = resource.split('?')
    partial_url = splitted_resource[0]
    try:
        parameters = splitted_resource[1]
    except:
        print 'no parameters recieved'

    if partial_url == '\\':
        url = os.curdir + '\\webroot' + DEFAULT_URL
    else:
        url = os.curdir + '\\webroot' + partial_url

    # TO DO: check if URL had been redirected, not available or other error code.
    redirected = False
    special = False
    if os.path.isfile(url):
        http_response = HTTP_VERSION + '200 ok\r\n'
        data = get_file_data(url)
        http_header = 'Content-Length: ' + str(len(data))
    elif url in REDIRECTION_DICTIONARY:
        redirected = True
        http_response = HTTP_VERSION + '302 Moved Temporarily\r\n'
        http_header = 'Content-Type: text/html' + '\r\nLocation: ' + REDIRECTION_DICTIONARY[url]\
                      + '\r\nstatus: 302' + HEADER_END  # TO DO: send 302 redirection response
        data = ''
    elif url in SPECIAL_DICTIONARY:
        special = True
        http_response = HTTP_VERSION + '200 ok\r\n'
        if SPECIAL_DICTIONARY[url] == 'next_num':
            data = get_next_num(parameters)
            http_header = 'Content-Length: ' + str(len(data))
            http_header += '\r\nContent-Type: text/html\r\ncharset=utf-8' + HEADER_END
        elif SPECIAL_DICTIONARY[url] == 'area':
            data = calaculate_area(parameters)
            http_header = 'Content-Length: ' + str(len(data))
            http_header += '\r\nContent-Type: text/html\r\ncharset=utf-8' + HEADER_END
            # SHLAIN: last 2 lines should be outside this if statement
    else:
        http_response = HTTP_VERSION + '404 Not Found\r\n'
        http_header = '\r\n'
        data = ''

    # TO DO: extract requested file type from URL (html, jpg etc)
    filetype = url[(url.rfind('.')+1):]
    if redirected or special:
        pass
    elif filetype == 'html':
        http_header += 'Content-Type: text/html\r\ncharset=utf-8' + HEADER_END  # TO DO: generate proper HTTP header
    elif filetype == 'jpg':
        http_header += 'Content-Type: image/jpeg' + HEADER_END  # TO DO: generate proper jpg header
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
    except: # SHLAIN: unnecessary
        valid_http =False
    if splitted_request.__len__() != 3:
        valid_http = False
    elif splitted_request[0] != 'GET':
        valid_http = False # SHLAIN: why do you have all those cases who are same ?
    elif not(http_version.startswith('HTTP/')) or not(http_version[http_version.find('/')+1].isdigit()) \
            or http_version[http_version.find('/')+2] != '.' or not(http_version[http_version.find('/')+3].isdigit()):
        # SHLAIN: too complicated if-statement
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
    print("Listening for connections on port %d" % PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        try:
            handle_client(client_socket)
        except socket.timeout:
            print('socket timed out')



if __name__ == "__main__":
    # Call the main handler function
    main()
