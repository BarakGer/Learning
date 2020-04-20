from scapy.all import *
load_layer("http")

''' Q5.4 '''

#my_packet = IP(dst="www.google.com") / Raw("blablabla")
#my_packet.show()
#send(my_packet)

'''used IP of http site'''
def one_site_filter(packet):
    return (HTTP in packet and ((packet[IP].src == "93.123.73.162") or (packet[IP].dst == "93.123.73.162")))


def print_summary(packet):
    print(packet.summary())


sniff(count=1, lfilter=one_site_filter, prn=print_summary)