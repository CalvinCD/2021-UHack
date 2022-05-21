#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

// Timers
unsigned long timer = 0;
float timeStep = 0.05;

// Pitch, Roll and Yaw values
float pitch = 0;
float roll = 0;
float yaw = 0;

const int pingPin = 8; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 9; // Echo Pin of Ultrasonic Sensor

void setup() {
  Serial.begin(115200);

  // Initialize MPU6050
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)) {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  // Calibrate gyroscope. The calibration must be at rest.
  // If you don't want calibrate, comment this line.
  mpu.calibrateGyro();
  // Set threshold sensivty. Default 3.
  // If you don't want use threshold, comment this line or set 0.
  mpu.setThreshold(3);
}

void loop() {
  timer = millis();

  long duration, inches, cm;
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(pingPin, LOW);
  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);
  cm = microsecondsToCentimeters(duration);

  
  // Read normalized values
  Vector norm = mpu.readNormalizeGyro();
  // Calculate Pitch, Roll and Yaw
  pitch = pitch + norm.YAxis * timeStep;
  roll = roll + norm.XAxis * timeStep;
  yaw = yaw + norm.ZAxis * timeStep;

  Serial.println(String(cm) + " " + String(pitch) + " " + String(roll) + " " + String(yaw));
  
  /*
  Serial.println(cm);
  Serial.println("x");
  Serial.println(pitch);
  Serial.println("x");
  Serial.println(roll);  
  Serial.println("x");
  Serial.println(yaw);
  */
  
  //Serial.println("this is a long test message. 1o23iu21o3ui1293123pj");
  

  // Wait to full timeStep period
  delay(max((timeStep*1000) - (millis() - timer), 0));
  
}

long microsecondsToCentimeters(long microseconds) {
   return microseconds / 29 / 2;
}
