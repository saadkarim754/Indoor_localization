#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>

#define SCAN_TIME 5 // seconds
float n = 2.0;
int txPower = -59; // typical BLE tx power at 1 meter

BLEScan* pBLEScan;

float rssiToDistance(int rssi) {
  return pow(10.0, ((float)(txPower - rssi)) / (10 * n));
}

struct Beacon {
  String name;
  float x, y;
  float distance = -1;
};

Beacon beacons[] = {
  {"Beacon_1", 0.0, 0.0},
  {"Beacon_2", 4.0, 0.0},
  {"Beacon_3", 2.0, 3.0}
};

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
  void onResult(BLEAdvertisedDevice advertisedDevice) {
    String devName = advertisedDevice.getName();
    int rssi = advertisedDevice.getRSSI();

    for (int i = 0; i < 3; i++) {
      if (devName == beacons[i].name) {
        beacons[i].distance = rssiToDistance(rssi);
        Serial.printf("Found %s with RSSI: %d → Distance: %.2f m\n",
                      devName.c_str(), rssi, beacons[i].distance);
      }
    }
  }
};

void trilaterateAndPrint() {
  Beacon b1 = beacons[0], b2 = beacons[1], b3 = beacons[2];
  float x1 = b1.x, y1 = b1.y, r1 = b1.distance;
  float x2 = b2.x, y2 = b2.y, r2 = b2.distance;
  float x3 = b3.x, y3 = b3.y, r3 = b3.distance;

  // Only compute if all distances are available
  if (r1 > 0 && r2 > 0 && r3 > 0) {
    float A = 2*(x2 - x1);
    float B = 2*(y2 - y1);
    float C = r1*r1 - r2*r2 - x1*x1 + x2*x2 - y1*y1 + y2*y2;

    float D = 2*(x3 - x2);
    float E = 2*(y3 - y2);
    float F = r2*r2 - r3*r3 - x2*x2 + x3*x3 - y2*y2 + y3*y3;

    float denominator = A*E - B*D;
    if (denominator != 0) {
      float x = (C*E - F*B) / denominator;
      float y = (C*D - A*F) / (B*D - A*E);
      Serial.printf("Estimated Location → X: %.2f, Y: %.2f\n\n", x, y);
    } else {
      Serial.println("❌ Trilateration failed (denominator is zero)");
    }
  } else {
    Serial.println("⏳ Waiting for all beacon distances...");
  }
}

void setup() {
  Serial.begin(115200);
  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99);
}

void loop() {
  for (int i = 0; i < 3; i++) {
    beacons[i].distance = -1; // Reset before scan
  }

  Serial.println("🔍 Scanning for beacons...");
  pBLEScan->start(SCAN_TIME, false);
  pBLEScan->clearResults();

  trilaterateAndPrint();

  delay(3000); // Wait before next scan cycle
}
