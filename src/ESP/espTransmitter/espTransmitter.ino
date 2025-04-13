#include <PulseSensorPlayground.h>
#include <Wire.h>
#include <Adafruit_AHTX0.h>

// pulse sensor object
const int PULSE_INPUT = 7;
const int THRESHOLD = 550;   
PulseSensorPlayground pulseSensor;  // Creates an object

// Create a custom I2C instance on GPIO 17 (SDA) and 16 (SCL)
TwoWire myWire = TwoWire(0);  // Use I2C bus 0 (can also be 1)
Adafruit_AHTX0 aht;

void setup() {
  Serial.begin(115200);
  delay(10);

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
  // sensors
  sensors_event_t humidity, temp;
  int myBPM;
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

  delay(1000); // update every 1 seconds
}