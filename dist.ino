
#define trigPin 4
#define echoPin 2
#define led 3 //red led 
#define led2 12 // green led

// motor one - rear wheels forward reverse
int enA = 10;
int in1 = 9;
int in2 = 8;
// motor two - left right
int enB = 5;
int in3 = 7;
int in4 = 6;


void setup() {
  Serial.begin (9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(led, OUTPUT);
  pinMode(led2, OUTPUT);
  
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  
}

void loop() {
  long duration, distance;
  digitalWrite(trigPin, LOW);  // Added this line
  delayMicroseconds(2); // Added this line
  digitalWrite(trigPin, HIGH);
//  delayMicroseconds(1000); - Removed this line
  delayMicroseconds(10); // Added this line
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;
  
  digitalWrite(in1, LOW); //digital high voltage - think of this as a constant
  digitalWrite(in2, HIGH);
  analogWrite(enA, 200); //when you are using anything other than the digital high voltage, so this goes to the pwm pins

  if (distance < 4) {  // This is where the LED On/Off happens

    digitalWrite(in1, HIGH); //digital high voltage - think of this as a constant
    digitalWrite(in2, LOW);
    analogWrite(enA, 255); //when you are using anything other than the digital high voltage, so this goes to the pwm pins
    
    digitalWrite(led,HIGH); // When the Red condition is met, the Green LED should turn off
    digitalWrite(led2,LOW);
  }

 else {
    digitalWrite(led,LOW);
    digitalWrite(led2,HIGH);
  }

  //Printing details to screen
  if (distance >= 200 || distance <= 0){
    Serial.println("Out of range");
  }
  else {
    Serial.print(distance);
    Serial.println(" cm");
  }
  delay(500);
}