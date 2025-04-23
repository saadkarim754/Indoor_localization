import time
import pywifi
import tkinter as tk
from tkinter import ttk
from pywifi import const

REFRESH_INTERVAL = 3000  # ms

def estimate_distance(rssi, tx_power=20, n=6):
    """Estimate distance in meters based on RSSI."""
    try:
        return round(10 ** ((tx_power - abs(rssi)) / (10 * n)), 2)
    except:
        return None

class WifiScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live WiFi RSSI & Distance Monitor")

        # Setup Treeview
        self.tree = ttk.Treeview(root, columns=("SSID", "RSSI", "Distance"), show="headings")
        self.tree.heading("SSID", text="SSID")
        self.tree.heading("RSSI", text="RSSI (dBm)")
        self.tree.heading("Distance", text="Estimated Distance (m)")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Init interface
        self.iface = pywifi.PyWiFi().interfaces()[0]
        self.update_wifi_list()

    def update_wifi_list(self):
        self.iface.scan()
        time.sleep(2)
        results = self.iface.scan_results()

        # Clear old rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        seen = set()
        for net in results:
            if net.ssid not in seen and net.ssid:
                seen.add(net.ssid)
                distance = estimate_distance(net.signal)
                self.tree.insert("", tk.END, values=(
                    net.ssid,
                    f"{net.signal} dBm",
                    f"{distance} m" if distance else "N/A"
                ))

        self.root.after(REFRESH_INTERVAL, self.update_wifi_list)

if __name__ == "__main__":
    root = tk.Tk()
    app = WifiScannerApp(root)
    root.mainloop()
