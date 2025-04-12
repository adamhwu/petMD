#include <PulseSensorPlayground.h>
#include <Wire.h>
#include <Adafruit_AHTX0.h>
#include <WiFi.h>
#include <WebSocketsClient.h>

const char* ssid = "Adam";
const char* password = "testing123";
const char* host = "11.27.2.195";  // IP of your PC running WebSocket server
const int PulseWire = 4;
int Threshold = 500;

WebSocketsClient webSocket;
PulseSensorPlayground pulseSensor;  // Creates an object

// Create a custom I2C instance on GPIO 17 (SDA) and 16 (SCL)
TwoWire myWire = TwoWire(0);  // Use I2C bus 0 (can also be 1)
Adafruit_AHTX0 aht;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_CONNECTED:
      Serial.println("Connected to server");
      webSocket.sendTXT("Hello from ESP32");
      break;
    case WStype_TEXT:
      Serial.printf("Received: %s\n", payload);
      break;
    case WStype_DISCONNECTED:
      Serial.println("Disconnected");
      break;
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println("we here");
  delay(10);
  // Initialize custom I2C pins
  myWire.begin(17, 16);  // SDA, SCL
  // Pass the custom Wire instance to the sensor
  if (!aht.begin(&myWire)) {
    Serial.println("Could not find AHT20 sensor, check wiring!");
    while (1) delay(10);
  }
  Serial.println("AHT20 sensor initialized successfully.");

  pulseSensor.analogInput(PulseWire);   
	pulseSensor.blinkOnPulse(IO38);       // Blink on-board LED with heartbeat
	pulseSensor.setThreshold(Threshold);   

  // wifi setup
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");

  webSocket.begin("11.27.2.195", 8080, "/");  // use "/" instead of "/ws"  webSocket.setReconnectInterval(5000);
}

void loop() {
  webSocket.loop();

  // wifi
  // Example: send something every 2s
  static unsigned long lastSend = 0;
  if (millis() - lastSend > 2000) {
    webSocket.sendTXT("Sensor data: 123");
    lastSend = millis();
  }

  // sensors
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp); // populate temp and humidity objects
  int myBPM = pulseSensor.getBeatsPerMinute();   

  Serial.print("Temperature: ");
  Serial.print(temp.temperature);
  Serial.println(" °C");

  Serial.print("Humidity: ");
  Serial.print(humidity.relative_humidity);
  Serial.println(" %");

  delay(1000); // update every 2 seconds
}