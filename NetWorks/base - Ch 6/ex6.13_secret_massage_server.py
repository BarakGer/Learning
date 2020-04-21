from scapy.all import *


def empty(packet):
    return (UDP in packet and packet[UDP].sport == 24601)

def action(packet):
    recieved_letter = chr(packet[UDP].dport)
    if recieved_letter != '/':
        print(recieved_letter)


def stop(packet):
    recieved_letter = chr(packet[UDP].dport)
    return recieved_letter == '/'

def main():
    """
    writing a secret message client for an existing server in "networks.cyber.org.il"
    """

    sniff(stop_filter=stop, lfilter=empty, prn=action)






if __name__ == '__main__':
    main()