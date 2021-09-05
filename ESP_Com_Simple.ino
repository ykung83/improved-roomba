#include <SoftwareSerial.h>
#include <Ultrasonic.h>
#include <Wire.h>

SoftwareSerial mySerial(2, 3);
Ultrasonic ultrasonic(12, 13);
Ultrasonic ultrasonic2(6, 7);

char a = 'a';
int x = 0;
String teststring = "";
boolean StringReady = false;
float currentHeading = 0;
float desiredHeading = 0;
int var1 = 0;
int var2 = 0;
int var3 = 0;
int var4 = 0;
int anglechange = 0;
int timestep = 0;
int distance = 0;
int accumDist = 0;
int startDist = 0;
boolean prevTurned = true;

void goForward(int t){
  digitalWrite(8, HIGH);
  digitalWrite(11, HIGH);
  delay(t);
  digitalWrite(11, LOW);
  digitalWrite(8, LOW);
  delay(1000);
}

void turnRight(int t){
  digitalWrite(11, HIGH);
  delay(t);
  digitalWrite(11, LOW);
}

void turnLeft(int t){
  digitalWrite(8, HIGH);
  delay(t);
  digitalWrite(8, LOW);
}

void rotateRightTime(int t){
  digitalWrite(11, HIGH);
  digitalWrite(9, HIGH);
  delay(t);
  digitalWrite(9, LOW);
  digitalWrite(11, LOW);
  delay(200);
}

void rotateLeftTime(int t){
  digitalWrite(10, HIGH);
  digitalWrite(8, HIGH);
  delay(t);
  digitalWrite(10, LOW);
  digitalWrite(8, LOW);
  delay(200);
}

void adjustForDrift(int dist){
  if(accumDist < 10){
    accumDist = 10;
  }
  if(dist > 65){
    return;
  }
  
  if(dist > startDist){
    turnRight(round(1650*atan(float(dist-startDist)/accumDist)));
  }
  else{
    turnLeft(round(1650*atan(float(startDist-dist)/accumDist)));
  }
  accumDist = 0;
  startDist = ultrasonic2.read(CM);
}

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  delay(5000);

  pinMode(8, OUTPUT);
  digitalWrite(8, LOW);
  pinMode(9, OUTPUT);
  digitalWrite(9, LOW);
  pinMode(10, OUTPUT);
  digitalWrite(10, LOW);
  pinMode(11, OUTPUT);
  digitalWrite(11, LOW);
}

void loop() {
  if(mySerial.available()>0){
    delay(50);
    while(mySerial.available()>0){
      a = mySerial.read();
      teststring += a;
    }

    var1 = teststring.charAt(3) - '0';
    var2 = teststring.charAt(4) - '0';
    var3 = teststring.charAt(5) - '0';
    var4 = teststring.charAt(6) - '0';
    timestep = var1*1000 + var2*100 + var3*10 + var4;
    
    if(teststring.charAt(0) == '0'){
      if(teststring.charAt(1) == '0'){
        goForward(timestep);
        prevTurned = false;
        accumDist = accumDist + round((timestep-40.4)*0.01353);
      }
      else if(teststring.charAt(1) == '1'){
        turnLeft(timestep);
        prevTurned = true;
        accumDist = 0;
      }
      else if(teststring.charAt(1) == '2'){
        rotateLeftTime(timestep); // In this case, angle
        prevTurned = true;
        accumDist = 0;
      }
    }
    else if(teststring.charAt(0) == '1'){
      if(teststring.charAt(1) == '0'){
        turnRight(timestep);
        prevTurned = true;
        accumDist = 0;
      }
      else if(teststring.charAt(1) == '2'){
        //Reverse left
        digitalWrite(9, HIGH);
        delay(timestep);
        digitalWrite(9, LOW);
        prevTurned = true;
        accumDist = 0;
      }
    }
    else if(teststring.charAt(0) == '2'){
      if(teststring.charAt(1) == '0'){  
        rotateRightTime(timestep);
        prevTurned = true;
        accumDist = 0;
      }
      else if(teststring.charAt(1) == '1'){
        //Reverse right
        digitalWrite(10, HIGH);
        delay(timestep);
        digitalWrite(10, LOW);
        prevTurned = true;
        accumDist = 0;
      }
      else if(teststring.charAt(1) == '2'){
        //Reverse straight
        digitalWrite(10, HIGH);
        digitalWrite(9, HIGH);
        delay(timestep);
        digitalWrite(10, LOW);
        digitalWrite(9, LOW);
        prevTurned = false;
        accumDist = 0;
      }
    }
    else if(teststring.charAt(0) == '3'){
      if(teststring.charAt(1) == '3'){
        distance = ultrasonic.read(CM);
        while(distance != timestep){
          if(distance > timestep){
            goForward(round(73.9*(distance-timestep)+40.4));
          }
          else{
            digitalWrite(10, HIGH);
            digitalWrite(9, HIGH);
            delay(round(73.9*(timestep-distance)+40.4));
            digitalWrite(10, LOW);
            digitalWrite(9, LOW);
          }
          distance = ultrasonic.read(CM);
          delay(500);
        }
        prevTurned = false;
        accumDist = 0;
      }
    }
    
    if(teststring.charAt(2) == '0'){
      delay(100);
    }
    else if(teststring.charAt(2) == '1'){
      mySerial.write("Received!");
    }
    else if(teststring.charAt(2) == '2'){
      delay(100);
    }
    else if(teststring.charAt(2) == '3'){
      distance = ultrasonic.read(CM);
      delay(100);
      mySerial.print(distance);
      mySerial.write(",");
      delay(500);
      distance = ultrasonic2.read(CM);
      delay(100);
      if(prevTurned){
        startDist = distance;
      }
      else{
        if(distance - startDist == 0){
          delay(50);
        }
        else if(abs(distance - startDist) <= 3){
          adjustForDrift(distance);
        }
        else{
          startDist = distance;
          accumDist = 0;
        }
      }
      mySerial.print(distance);
      mySerial.write("!");
    }
    
    teststring = "";
  }
  delay(50);
}
