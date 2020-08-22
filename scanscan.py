import scapy.all as scapy
import subprocess
import time
from dotenv import load_dotenv
import os

load_dotenv()

network = os.getenv("TARGET_IP")
mac = os.getenv("TARGET_MAC")

def scan(ip):
    arp_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast_packet = broadcast_packet/arp_packet
    answered_list = scapy.srp(arp_broadcast_packet, timeout=1, verbose=False)[0]
    client_list = []

    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)

    return client_list

path_to_notepad = 'C:\\Windows\\System32\\notepad.exe'
path_to_file = 'C:\\Users\\jacob\\Desktop\\Do things.txt'

def print_result(scan_list):
    print("IP\t\t\tMAC\n----------------------------------------")
    for client in scan_list:
        print(client["ip"] + "\t\t" + client["mac"])
        if client["mac"] == mac:
            subprocess.call([path_to_notepad, path_to_file])

for i in range(10):
    result_list = scan(network)
    print_result(result_list)
    time.sleep(3)

