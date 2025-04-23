import time
import pywifi
import tkinter as tk
from tkinter import ttk
from pywifi import const

REFRESH_INTERVAL = 3000  # milliseconds (3 seconds)

class WifiScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live WiFi RSSI Monitor")

        # Set up TreeView
        self.tree = ttk.Treeview(root, columns=("SSID", "RSSI"), show="headings")
        self.tree.heading("SSID", text="SSID")
        self.tree.heading("RSSI", text="RSSI (dBm)")
        self.tree.pack(fill=tk.BOTH, expand=True)

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
            if net.ssid not in seen and net.ssid:  # Ignore blank SSIDs
                seen.add(net.ssid)
                self.tree.insert("", tk.END, values=(net.ssid, f"{net.signal} dBm"))

        self.root.after(REFRESH_INTERVAL, self.update_wifi_list)

if __name__ == "__main__":
    root = tk.Tk()
    app = WifiScannerApp(root)
    root.mainloop()
