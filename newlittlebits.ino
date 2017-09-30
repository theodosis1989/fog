const int buttonPin = A0;  //arduino leonardo
const int buttonFogPin = A1;
const int barPin = 5;   //arduino leonardo
const int barPinClick = 1;
const int topButtonPin = 0; //arduino leonardo
const int i = 0;
String mystring;
char c;
String isFog;
bool newVal = false;
String cmp;
unsigned long timerA;

int buttonState = 0;
int buttonFogState = 0;
int topButtonState = 0;

bool FogIsOn = false;
bool IsPullFinished = false;

void setup() {
  // initialize the Servo as an output:
  pinMode(barPin, OUTPUT);
  pinMode(barPinClick, OUTPUT);

  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
  pinMode(buttonFogPin, INPUT);
  pinMode(topButtonPin, INPUT);

  analogWrite(1, 0);
}

void blinkled()
{
  analogWrite(9, 1000);
  delay(100);
  analogWrite(9, 0);
  delay(100);
}

void getInput()
{
  blinkled();
  
  while (Serial.available() > 0) {
    char c = Serial.read();  //gets one byte from serial buffer
    mystring += c; //makes the string readString
    newVal = true;

    if(newVal == true)
    {
      isFog = String(mystring);
      isFog.trim();
      mystring = "";
      newVal = false;
      
      if(isFog.equals("f")) {
        IsPullFinished = true;
      }
      else {
        blinkled();
//        Serial.print("L");
      }
    }
  }
}


void loop() {

  buttonState = digitalRead(buttonPin);
  buttonFogState = digitalRead(buttonFogPin);
  topButtonState = digitalRead(topButtonPin);
  delay(100);

  if (buttonFogState == HIGH) {
    if(FogIsOn) {
      FogIsOn = false;
    }
    else {
      FogIsOn = true;
    }
  }

  if(FogIsOn) {
    analogWrite(9, 1000);
    delay(200);
  }
  else {
    analogWrite(9, 0);
    delay(200);
  }

  if(topButtonState == HIGH)
  {
    timerA = millis();
    analogWrite(1, 1000);
    delay(200);
    analogWrite(1, 0);
    
    Serial.print("p");
    FogIsOn = false;
    analogWrite(9, 0);
    IsPullFinished = false;
    while(!IsPullFinished || (millis() - timerA) > 90000 ){

      if((millis() - timerA) > 90000)
      {
        FogIsOn = false;
        break;
      }
      getInput();
      FogIsOn = true;
    }
    delay(600);
  }
  
  if (buttonState == HIGH) {
      analogWrite(1, 1000);
//      isFog.trim();
//      Serial.print("b");
//      cmp = String("c");
//    Serial.println(FogIsOn);
    if(FogIsOn == false)
    {
      analogWrite(5, 1000);
      delay(600); 
    }
    else
    {
      Serial.print("b");
      analogWrite(5, 0);
      delay(600);
    }
  }
  else {
    analogWrite(1, 0);
    analogWrite(5, 0);
  } 
}
