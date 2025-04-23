#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

void setup() {
  Serial.begin(115200);

  // Initialize BLE
  BLEDevice::init("Beacon_1");  // Each ESP32 beacon should have a unique name like Beacon_1, Beacon_2, etc.
  BLEServer *pServer = BLEDevice::createServer();
  
  // Start advertising
  BLEAdvertising *pAdvertising = pServer->getAdvertising();
  pAdvertising->start();
}

void loop() {
  // In the loop, you can add functionality if needed, but here it just advertises continuously.
  delay(1000);
}
