    /*
    * Ultrasonic Sensor HC-SR04 and Arduino Tutorial
    *
    * by Dejan Nedelkovski,
    * www.HowToMechatronics.com
    *
    */
    // defines pins numbers
    const int trigPinForward = 3;
    const int echoPinForward = 2;
    const int trigPinLeft    = 5;
    const int echoPinLeft    = 4;
    const int trigPinRight   = 7;
    const int echoPinRight   = 6;
    const int upPinRev       = 8;
    
    
    const int ledPin = 11;
    
    // defines variables
    long duration;
    byte distance;
    byte distanceF;
    byte distanceL;
    byte distanceR;
    byte obstacleU;
    
    void setup() {
    pinMode(trigPinForward,  OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPinForward,  INPUT); // Sets the echoPin as an Input
    pinMode(trigPinLeft,     OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPinLeft,     INPUT); // Sets the echoPin as an Input
    pinMode(trigPinRight,    OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPinRight,    INPUT); // Sets the echoPin as an Input
    pinMode(upPinRev,        INPUT); // Sets the trigPin as an Output
    pinMode(ledPin,          OUTPUT);
    Serial.begin(115200); // Starts the serial communication
    digitalWrite(ledPin,HIGH);
    
    digitalWrite(trigPinForward, LOW);
    digitalWrite(trigPinLeft, LOW);
    digitalWrite(trigPinRight, LOW);
    }
    inline void getUltrasonic(const int trig, const int echo){
    //delay(10);
      //delayMicroseconds(2); //was 2
    // Sets the trigPin on HIGH state for 10 micro seconds
      digitalWrite(trig, HIGH);
      delayMicroseconds(10);
      digitalWrite(trig, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
      duration = pulseIn(echo, HIGH);
    // Calculating the distance
      distance= min(255,duration*0.034/2);
    // Calculating the distance and returning
    }
    void loop() {
    // Clears the trigPin
    //distance = 11;
    distanceF = 2;
    getUltrasonic(trigPinForward,echoPinForward);
    distanceF = max(2,distance);
    //Serial.write(distance);
    distanceL = 2;
    getUltrasonic(trigPinLeft,echoPinLeft);
    distanceL = max(2,distance);
    //Serial.write(distance);
    
    distanceR = 2;
    getUltrasonic(trigPinRight,echoPinRight);
    distanceR = max(2,distance);
    //Serial.write(distance);
    
    //Serial.write();
    obstacleU = 0; //digitalRead(upPinRev);
    /*
    digitalWrite(trigPinForward, LOW);
    //delay(10);
    delayMicroseconds(2); //was 2
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPinForward, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPinForward, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPinForward, HIGH);
    // Calculating the distance
    distance= min(255,duration*0.034/2);
    // Prints the distance on the Serial Monitor
    //analogWrite(ledPin,max(0,200-distance*5));
    */
    
    //Serial.print("Distance: ");
    
    Serial.write(distanceF);
    Serial.write(distanceR);
    Serial.write(distanceL);
    Serial.write(obstacleU);
    }
