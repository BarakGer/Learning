from scapy.all import *

def main():
    """
    writing a secret message client for an existing server in "networks.cyber.org.il"
    """
    wanted_message = 'Hello/'
    for char in wanted_message:
        char_port = ord(char)
        packet = IP(dst="127.0.0.1") / UDP(sport=24601, dport=char_port) / Raw('')
        send(packet)



if __name__ == '__main__':
    main()