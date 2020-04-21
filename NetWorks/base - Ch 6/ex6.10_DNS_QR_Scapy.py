from scapy.all import *

# build dns packet layers and send it
dns_packet = IP(dst="8.8.8.8") / UDP(sport=24601, dport=53) / DNS(qdcount=1) / DNSQR(qname='www.google.com')
response_packet = sr1(dns_packet)
print(response_packet[DNSRR].rdata)