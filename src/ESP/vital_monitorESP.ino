#include <WebSocketsClient.h>
#include <WiFi.h>
#include <Arduino_JSON.h>

#include <PulseSensorPlayground.h>
#include <Wire.h>
#include <Adafruit_AHTX0.h>

// web stuff
const char* ssid = "SSID";            // fill in with local network name and password
const char* password = "PASSWORD";
unsigned long previousMillis = 0;     // last time you sent something
const long interval = 1000;           // interval at which to send (ms)

// sensor stuff
// pulse sensor object
const int PULSE_INPUT = 7;
const int THRESHOLD = 550;   
sensors_event_t humidity, temp;
int myBPM;
PulseSensorPlayground pulseSensor;  // Creates an object

// Create a custom I2C instance on GPIO 17 (SDA) and 16 (SCL)
TwoWire myWire = TwoWire(0);  // Use I2C bus 0 (can also be 1)
Adafruit_AHTX0 aht;

// web stuff
WebSocketsClient webSocket;

String jsonConvert(){
  String jsonString = JSON.stringify(34);
  return jsonString;
}


void setup() {
  Serial.begin(115200);
  delay(10);

  // wifi initialization
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  // fill in computer IP address of server
  webSocket.begin("<Server_IP_Addr>", 8765, "/ws");

  // sensor stuff
  // Initialize custom I2C pins
  myWire.begin(17, 16);  // SDA, SCL

  // pulseSensor values
  pulseSensor.analogInput(PULSE_INPUT);   
	pulseSensor.setThreshold(THRESHOLD); 

  if (pulseSensor.begin()) {
    Serial.println("We created a pulseSensor Object !");  //This prints one time at Arduino power-up,  or on Arduino reset.  
  }

  // check temp sensor connection
  if (!aht.begin(&myWire)) {
    Serial.println("Could not find AHT20 sensor, check wiring!");
    while (1) delay(10);
  }
  Serial.println("AHT20 sensor initialized successfully.");
}

void loop() {
  // unsigned long currentMillis = millis();
  // if (currentMillis - previousMillis >= interval) {
  //   previousMillis = currentMillis;  
  String json = JSON.stringify("{\"type\":\"sensor\",\"temperature\":" + String(temp.temperature) + ", \"humidity\":" + String(humidity.relative_humidity)+ ", \"pulse\":" + String(myBPM)+"}");

  webSocket.sendTXT(json);
  Serial.println("sent");

  aht.getEvent(&humidity, &temp); // populate temp and humidity objects
  if (pulseSensor.sawStartOfBeat()) {
    myBPM = pulseSensor.getBeatsPerMinute();
  }

  Serial.print("Temperature: ");
  Serial.print(temp.temperature);
  Serial.println(" °C");

  Serial.print("Humidity: ");
  Serial.print(humidity.relative_humidity);
  Serial.println(" %");

  Serial.print("Heartbeat: ");
  Serial.print(myBPM);
  Serial.println(" BPM");
// }
  webSocket.loop();
}