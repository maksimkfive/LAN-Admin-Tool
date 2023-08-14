import asyncio

from database_handler import DatabaseHandler
from network_tools import NetworkTools

class NetworkAdminTool:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.current_hosts = []

    def show_commands(self):
        print("\nAvailable Commands:")
        print("scan              - Scan the network for hosts.")
        print("lookup [seq]      - Lookup details of a host by sequence number.")
        print("arp [target_ip]   - ARP spoof the specified target IP address.")
        print("cc                - Clear the cache.")
        print("exit              - Exit the program.")
        print("help              - Show available commands.")
        print("\n")

    def start(self):
        self.show_commands()
        while True:
            command = input(">> ").lower().strip()
            if command == "scan":
                asyncio.run(self.scan_network())
            elif command.startswith("lookup"):
                _, seq = command.split()
                asyncio.run(self.lookup_host(int(seq)))
            elif command.startswith("arp"):
                _, target_ip = command.split()
                NetworkTools.arp_spoof(target_ip, "192.168.0.1")  # Assuming default gateway is 192.168.0.1
            elif command == "cc":
                self.clear_cache()
            elif command == "help":
                self.show_commands()
            elif command == "exit":
                break
            else:
                print("Unknown command. Please try again.")

    async def scan_network(self):
        hosts = await NetworkTools.scan_network()
        self.current_hosts = []
        print("\nDetected Hosts:")
        for index, host in enumerate(hosts, 1):
            host_id = self.db_handler.save_host(host, "Unknown MAC")
            self.current_hosts.append(host_id)
            print(f"{index}. IP: {host}")
        print("\n")

    async def lookup_host(self, seq):
        if seq > len(self.current_hosts):
            print("Invalid sequence number.")
            return

        host_id = self.current_hosts[seq - 1]
        host_data = self.db_handler.get_host_details(host_id)

        # Retrieve the correct IP address based on the host_id
        host_ip = [h[1] for h in self.db_handler.get_all_hosts() if h[0] == host_id][0]

        if not host_data:
            details = await NetworkTools.retrieve_info(host_ip)
            print("\nHost Details:")
            print(details)
        else:
            print("\nHost Details from Cache:")
            for data in host_data:
                print(f"Port: {data[1]}, Service: {data[2]}")
        print("\n")

    def clear_cache(self):
        self.db_handler.clear_cache()
        print("Cache cleared.")

if __name__ == "__main__":
    tool = NetworkAdminTool()
    tool.start()
