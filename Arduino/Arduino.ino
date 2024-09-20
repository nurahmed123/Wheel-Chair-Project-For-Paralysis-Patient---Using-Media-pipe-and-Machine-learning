// Motor driver connections
#define IN1 6
#define IN2 5
#define IN3 4
#define IN4 3
#define ENA 7
#define ENB 2

char command;  // Variable to store Bluetooth command

void setup() {
  // Set all the motor control pins to output
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  
  // Start serial communication for Bluetooth at 9600 baud rate
  Serial.begin(9600);
}

void loop() {
  // Check if any data is available from the Bluetooth module
  if (Serial.available() > 0) {
    command = Serial.read();  // Read the command
    controlCar(command);      // Control the car based on the command
  }
}

void controlCar(char command) {
  switch (command) {
    case 'forward':  // Move forward
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      analogWrite(ENA, 255);  // Full speed for motor A
      analogWrite(ENB, 255);  // Full speed for motor B
      break;
      
    case 'backward':  // Move backward
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      analogWrite(ENA, 255);  // Full speed for motor A
      analogWrite(ENB, 255);  // Full speed for motor B
      break;
      
    case 'left':  // Turn left
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      analogWrite(ENA, 200);  // Medium speed for motor A
      analogWrite(ENB, 255);  // Full speed for motor B
      break;
      
    case 'right':  // Turn right
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      analogWrite(ENA, 255);  // Full speed for motor A
      analogWrite(ENB, 200);  // Medium speed for motor B
      break;
      
    case 'stop':  // Stop
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
      break;
      
    default:   // Stop for any other input
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
      break;
  }
}
