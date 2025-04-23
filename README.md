# 📍 RSSI-Based Indoor Localization Using WiFi & Edge Impulse

> Real-time indoor localization for mobile robots using WiFi signal strength and machine learning.

---

## 🧠 Introduction

Indoor localization is crucial for robotics, automation, and smart IoT systems where GPS is unreliable. This project uses **RSSI (Received Signal Strength Indicator)** values from WiFi access points or ESP32s placed at known positions to estimate the real-time location of a mobile agent (like an RC car).

This method is based on:
- **Trilateration using RSSI values**
- **Machine learning for position prediction**
- **Edge Impulse** for model training and deployment

The system is designed to work with any WiFi-capable device (like ESP32s or phones) as fixed signal sources (anchors) and an ESP32 on a mobile robot as the scanning receiver.

---

## 📐 How RSSI Localization Works

### 🔹 RSSI Basics

RSSI represents how strong a signal is received from a transmitter. It typically ranges from -30 dBm (strong) to -90 dBm (weak). As signal strength decreases with distance, you can **estimate distance** from the RSSI using this formula:

```text
distance = 10 ^ ((TxPower - RSSI) / (10 * n))
```

Where:
- `TxPower` is the known transmit power (usually ≈ 20 dBm)
- `n` is the path-loss exponent (environment dependent: 2–4)

### 🔹 Trilateration

Using **3+ fixed WiFi devices** with known positions, and the RSSI-based distances to each, you can estimate the receiver's position in 2D space using trilateration.

Example layout:
```
A(0,0)     B(d,0)
     \
      \
       \
       C(x,y)  ← robot with ESP32 measuring RSSI
```

You convert RSSI values to distances from each anchor, then solve equations to find (x, y).

---

## 🧪 Experimental Setup

### ⚙ Requirements

- 3+ ESP32 boards or WiFi-enabled phones broadcasting SSIDs
- A laptop or ESP32 scanning RSSI values
- A floor grid to mark known (x, y) positions
- Python 3 (for GUI + data collection)
- Edge Impulse account (for model training)

### 📁 Python Scripts

1. **`wifi_scan_gui.py`** — Scans all visible SSIDs and displays their RSSI values in a live-updating GUI.
2. **`wifi_distance_gui.py`** — Enhances the above by estimating distance using path loss model.
3. **`data_logger_gui.py`** — Lets you scan only target SSIDs and manually enter `(x, y)` positions. Saves readings to `rssi_data.csv`.

---

## 🚀 Getting Started

### 🧰 Install Dependencies

```bash
pip install pywifi
```

On Windows also install:
```bash
pip install comtypes
```

### 📡 Running the Logger GUI

```bash
python data_logger_gui.py
```

1. Set your target SSIDs in the `TARGET_SSIDS` list in the script.
2. Place your device at a known point in the room.
3. Click "Take Reading", enter X and Y, and repeat across multiple locations.
4. Close the GUI to save `rssi_data.csv`.

---

## 🧠 Training the Model (Edge Impulse)

1. Go to [Edge Impulse](https://edgeimpulse.com/)
2. Create a new project
3. Upload `rssi_data.csv` as a **regression dataset**
   - Input features: RSSI values
   - Output: x and y coordinates
4. Train a regression model (fully connected or decision tree works well)
5. Deploy the model to your ESP32 (or use Python SDK for testing)

---

## 🐾 Real-World Applications

- Indoor tracking of **RC cars**
- Locating **robotic dogs** in smart homes
- Guiding **autonomous drones** indoors
- Monitoring pets or wearable devices for **elderly care**
- Interactive localization in **smart museums**

---

## 📚 Related Research

This project was inspired by the IEEE paper:

**"RSSI-Based Indoor Localization with the Internet of Things"**  
Sebastian Sadowski & Petros Spachos, IEEE Access, 2018  
[🔗 Read the full paper](https://www.researchgate.net/publication/325561044)

**Key Insights:**
- RSSI is easy to implement but prone to noise
- WiFi offers wide coverage but uses more power
- Trilateration can achieve ~0.6 m accuracy with proper tuning
- Environment calibration (walls, glass) matters a lot

---

## 📎 Libraries Used

- `pywifi` – for WiFi scanning
- `tkinter` – GUI toolkit
- `csv` – saving data
- `time` – handling delays

---

## 🙌 Contribution & Future Work

Feel free to fork and extend:
- Add live plotting or heatmaps
- Use Kalman Filters to smooth RSSI noise
- Add support for BLE or Zigbee anchors

PRs and feedback welcome!

---

## 🔒 License

MIT License. Free to use and modify for research or personal projects.
