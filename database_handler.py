import sqlite3

class DatabaseHandler:
    def __init__(self, db_name="network_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS Hosts (
                    id INTEGER PRIMARY KEY,
                    ip TEXT NOT NULL,
                    mac TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS HostDetails (
                    host_id INTEGER,
                    port INTEGER,
                    service TEXT,
                    FOREIGN KEY(host_id) REFERENCES Hosts(id)
                )
            """)

    def save_host(self, ip, mac):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO Hosts (ip, mac) VALUES (?, ?)", (ip, mac))
            return cur.lastrowid

    def save_host_details(self, host_id, port, service):
        with self.conn:
            self.conn.execute("INSERT INTO HostDetails (host_id, port, service) VALUES (?, ?, ?)",
                              (host_id, port, service))

    def get_all_hosts(self):
        with self.conn:
            return self.conn.execute("SELECT * FROM Hosts").fetchall()

    def get_host_details(self, host_id):
        with self.conn:
            return self.conn.execute("SELECT * FROM HostDetails WHERE host_id=?", (host_id,)).fetchall()

    def clear_cache(self):
        with self.conn:
            self.conn.execute("DELETE FROM HostDetails")
            self.conn.execute("DELETE FROM Hosts")
