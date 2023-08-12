from database_handler import DatabaseHandler
from network_tools import NetworkScanner, HostAnalyzer, arp_spoof, limit_bandwidth

class NetworkAdminTool:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.current_hosts = []
        self.connection_times = {}  # Store connection times for detected hosts

    def show_commands(self):
        print("\nAvailable Commands:")
        print("scan              - Scan the network for hosts.")
        print("lookup [seq]      - Lookup details of a host by sequence number.")
        print("cc                - Clear the cache.")
        print("cut [ip] [limit]  - Limit bandwidth for given IP to the specified percentage.")
        print("exit              - Exit the program.")
        print("help              - Show available commands.")
        print("\n")

    def start(self):
        self.show_commands()
        while True:
            command = input(">> ").lower().strip()
            if command == "scan":
                self.scan_network()
            elif command.startswith("lookup"):
                _, seq = command.split()
                self.lookup_host(int(seq))
            elif command == "cc":
                self.clear_cache()
            elif command.startswith("cut"):
                _, target_ip, percentage = command.split()
                self.cut(target_ip, int(percentage))
            elif command == "help":
                self.show_commands()
            elif command == "exit":
                break
            else:
                print("Unknown command. Please try again.")

    def scan_network(self):
        scanner = NetworkScanner()
        hosts = scanner.scan_network()
        self.current_hosts = []

        print("\nDetected Hosts:")
        for index, host in enumerate(hosts, 1):
            ip = host["ip"]
            mac = host["mac"]

            # Save to database
            host_id = self.db_handler.save_host(ip, mac)
            self.current_hosts.append(host_id)

            print(f"{index}. IP: {ip}, MAC: {mac}")
        print("\n")

    def lookup_host(self, seq):
        if seq > len(self.current_hosts):
            print("Invalid sequence number.")
            return

        host_id = self.current_hosts[seq - 1]
        host_data = self.db_handler.get_host_details(host_id)

        if not host_data:
            host = self.db_handler.get_all_hosts()[seq - 1]
            analyzer = HostAnalyzer(host[1])

            open_ports = analyzer.quick_scan()
            details = analyzer.retrieve_info()

            for port in open_ports:
                self.db_handler.save_host_details(host_id, port, "Unknown")

            host_data = self.db_handler.get_host_details(host_id)

        print("\nHost Details:")
        for data in host_data:
            print(f"Port: {data[1]}, Service: {data[2]}")
        print("\n")

    def clear_cache(self):
        self.db_handler.clear_cache()
        print("Cache cleared.")

    def cut(self, target_ip, percentage):
        gateway_ip = "192.168.0.1"
        arp_spoof(target_ip, gateway_ip)
        limit_bandwidth(target_ip, percentage)

if __name__ == "__main__":
    tool = NetworkAdminTool()
    tool.start()
