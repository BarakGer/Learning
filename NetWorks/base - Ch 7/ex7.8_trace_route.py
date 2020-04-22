from scapy.all import *
import sys

DESTINATION = sys.argv[1]
TIMEOUT = 3
IP_DICT = {}

def main():
    """
    writing a trace route function
    """
    dest = 'www.google.com'
    first = True
    replied = False
    TTL = 1
    SEQ = 100

    while first or not(replied):
        first = False
        my_packet = IP(dst=DESTINATION, ttl=TTL) /ICMP(id=1, seq=SEQ) / Raw('abc')

        try:
            response_packet = sr1(my_packet, timeout=TIMEOUT)
            IP_DICT[TTL] = response_packet[IP].src
            #print('after {} hops is: {}'.format(TTL, response_packet[IP].src))
            if (ICMP in response_packet and response_packet[ICMP].type == 0):
                replied = True
        except:
            IP_DICT[TTL] = 'NO RESPONSE'

        TTL += 1
        SEQ += 1
    for i in IP_DICT:
        print('after {} hops is: {}'.format(i, IP_DICT[i]))
    print('arrived to {}'.format(DESTINATION))




if __name__ == '__main__':
    main()