# 📍 RSSI-Based Indoor Localization Using WiFi & BLE

> Real-time indoor localization for mobile robots using either WiFi signal strength and machine learning or a simple BLE-based trilateration approach.

---

## 🧠 Introduction

Indoor localization is critical for robotics, automation, and IoT systems where GPS fails. This project implements **two parallel methods** to estimate the real-time position of a mobile robot using RSSI (Received Signal Strength Indicator):

- **WiFi + Machine Learning (Edge Impulse)**  
- **BLE + Onboard Trilateration**

These methods use fixed ESP32s (or access points) as signal anchors and another ESP32 on the mobile agent as a receiver.

---

## 📁 Project Structure

```text
📦 RSSI_Localization_Project
├── 📂 RSSI_using_wifi      # WiFi-based scanning & ML training (run on PC)
└── 📂 RSSI_using_BLE       # BLE-based trilateration (run directly on ESP32)
```

---

## 📶 RSSI_using_wifi

This approach uses WiFi scanning on a laptop or PC to collect RSSI values and train a **machine learning model** using **Edge Impulse**.

### 📜 Purpose
To create a trained regression model that predicts location `(x, y)` from RSSI values.

### 🧰 Requirements

- Python 3
- `pywifi`, `tkinter`, `comtypes` (on Windows)

### 🗃 Key Scripts

- `RSSI_measurement.py` – GUI to scan and display visible SSIDs & RSSI
- `distance_measurement.py` – Adds distance estimation from RSSI
- `data_set_development_for_training_model.py` – Logs labeled (x, y, RSSI) data for training

### 🧠 ML Pipeline (Edge Impulse)

1. Collect dataset with known positions
2. Upload `rssi_data.csv` to Edge Impulse
3. Train a regression model
4. Deploy to ESP32 or test using Python

---

## 🔵 RSSI_using_BLE

This approach runs **entirely on the ESP32**, using BLE signals from 3 fixed beacons to estimate position using **RSSI → distance → trilateration**.

### 📜 Purpose
Simple, real-time indoor localization directly on ESP32 — no model training needed.

### 📌 Assumptions

- 3 ESP32 beacons broadcasting with names: `"Beacon_1"`, `"Beacon_2"`, `"Beacon_3"`
- Each beacon is at a known (x, y) location
- One receiver ESP32 scans RSSI from beacons, converts to distance, and applies trilateration

### 🗂 Files

- `esp32_ble_receiver.ino` – Main sketch running on receiver ESP32
- (Optional) `esp32_beacon.ino` – Sketch for BLE broadcaster ESP32s

### 🔢 Trilateration Formula

Based on converting RSSI to distance:

```text
distance = 10 ^ ((TxPower - RSSI) / (10 * n))
```

Then solving for (x, y) using 2D trilateration equations.

---

## 🚀 Use Cases

- **Indoor tracking of RC cars**
- **Autonomous robot navigation**
- **IoT device geofencing**
- **Interactive smart environments**

---

## 🧪 Accuracy Tips

- Calibrate `TxPower` and `n` for your room
- Avoid signal obstructions (metal, walls)
- Average multiple RSSI readings per beacon
- WiFi method is more accurate but requires model training
- BLE method is more portable and quick to run on-device

---

## 📚 Related Research

**"RSSI-Based Indoor Localization with the Internet of Things"**  
Sebastian Sadowski & Petros Spachos, IEEE Access, 2018  
[🔗 Full Paper](https://www.researchgate.net/publication/325561044)

---

## 📎 Dependencies

- `pywifi`, `tkinter`, `csv` (for WiFi GUI)
- Arduino `ESP32 BLE` libraries (for BLE method)

---

## 🙌 Contribution & Future Work

- Add Kalman Filtering to BLE
- Add GUI map overlay of position
- Extend to Zigbee/UWB support

PRs welcome!

---

## 🔒 License

MIT License — free to use and modify for personal or academic projects.
