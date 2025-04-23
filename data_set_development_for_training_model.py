import time
import pywifi
import tkinter as tk
from tkinter import ttk
import csv

# === CONFIG ===
TARGET_SSIDS = ["eduroam", "Saadi", "ESP_3"]  # Replace with your target SSIDs
REFRESH_TIME = 2  # Seconds to wait for scan
DATA_FILE = "rssi_data.csv"

# CSV Setup
header = TARGET_SSIDS + ["x", "y"]
data_log = []

# Function to scan WiFi and return RSSI for target SSIDs
def scan_targets(iface):
    iface.scan()
    time.sleep(REFRESH_TIME)
    results = iface.scan_results()

    # Print all visible networks
    print("\n[Scan Result] All Visible Networks:")
    available_ssids = []
    for net in results:
        print(f"SSID: {net.ssid}, RSSI: {net.signal} dBm")
        available_ssids.append(net.ssid)

    # Map RSSI for target SSIDs
    rssi_dict = {ssid: None for ssid in TARGET_SSIDS}
    for ssid in TARGET_SSIDS:
        matched = False
        for net in results:
            if net.ssid == ssid:
                rssi_dict[ssid] = net.signal
                matched = True
                break
        if not matched:
            print(f"[WARN] Target SSID '{ssid}' not found in scan.")

    return rssi_dict

# GUI App
class RSSICollectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi RSSI Data Collector")
        self.iface = pywifi.PyWiFi().interfaces()[0]

        # Table view
        self.tree = ttk.Treeview(root, columns=("SSID", "RSSI"), show="headings")
        self.tree.heading("SSID", text="SSID")
        self.tree.heading("RSSI", text="RSSI (dBm)")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Entry for x, y
        entry_frame = tk.Frame(root)
        entry_frame.pack()

        tk.Label(entry_frame, text="X:").pack(side=tk.LEFT)
        self.x_entry = tk.Entry(entry_frame, width=5)
        self.x_entry.pack(side=tk.LEFT)

        tk.Label(entry_frame, text="Y:").pack(side=tk.LEFT)
        self.y_entry = tk.Entry(entry_frame, width=5)
        self.y_entry.pack(side=tk.LEFT)

        # Button to take a reading
        self.scan_button = tk.Button(root, text="Take Reading", command=self.take_reading)
        self.scan_button.pack(pady=10)

        # Save on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def take_reading(self):
        rssi_data = scan_targets(self.iface)

        # Clear and update GUI
        for row in self.tree.get_children():
            self.tree.delete(row)
        for ssid in TARGET_SSIDS:
            rssi_val = rssi_data[ssid] if rssi_data[ssid] is not None else "N/A"
            self.tree.insert("", tk.END, values=(ssid, rssi_val))

        # Get x, y input
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
        except ValueError:
            print("❌ Invalid X, Y input. Please enter numeric values.")
            return

        # Store to memory
        row = [rssi_data.get(ssid, "") for ssid in TARGET_SSIDS] + [x, y]
        data_log.append(row)
        print("✅ Logged:", row)

        # Clear inputs
        self.x_entry.delete(0, tk.END)
        self.y_entry.delete(0, tk.END)

    def on_close(self):
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data_log)
        print(f"\n📁 Saved all data to {DATA_FILE}")
        self.root.destroy()

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = RSSICollectorApp(root)
    root.mainloop()
