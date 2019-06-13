// Enable debug prints to serial monitor
#define MY_DEBUG
#define MY_DEBUG_VERBOSE
#define MY_REGISTRATION_FEATURE 1
#define MY_NODE_ID 9
//#define MY_PARENT_ID 9
// Enable and select radio type attached
#define MY_RADIO_RF24
//#define MY_RF24_DATARATE RF24_250KBPS
//#define MY_RF24_BASE_RADIO_ID 0x01,0xFC,0xE1,0xA8,0xA9
#define MY_RF24_CHANNEL 124
//#define MY_RADIO_NRF5_ESB
//#define MY_RADIO_RFM69
//#define MY_RADIO_RFM95
//#define MY_SIGNING_SIMPLE_PASSWD "123456789012345678901234567890"
//#define MY_SIGNING_REQUEST_SIGNATURES
// Set blinking period
//#define MY_DEFAULT_LED_BLINK_PERIOD 300
#define MY_MQTT_CLIENT_PUBLISH_RETAIN
#include <MySensors.h>

// First we include the libraries
#include <SPI.h>
#define MAX6675_CS   6 //9
#define MAX6675_SO   7 //8
#define MAX6675_SCK  5 //10
#define READ_SAMPLE_INTERVAL (10)    // define how many samples you are going to take in normal operation
#define READ_SAMPLE_TIMES    (20)   // define the time interval(in milliseconds) between each samples in

#define   CHILD_ID_TEMP 4
#define   CHILD_ID_MOTION 5
/********************************************************************/
uint32_t SLEEP_TIME = 2000; // Sleep time between reads (in milliseconds)


//VARIABLES
int16_t lastTemp;
int16_t temp;

MyMessage msg_TEMP(CHILD_ID_TEMP, V_TEMP);
MyMessage msg_MOTION(CHILD_ID_MOTION, V_LEVEL);

void setup()
{
  Serial.begin(115200);
  // Start up the library 

}

void presentation()
{
  // Send the sketch version information to the gateway and Controller
  sendSketchInfo("HighTemp_Motion Control Sensor", "1.0");

  // Register all sensors to gateway (they will be created as child devices)
  present(CHILD_ID_TEMP, S_TEMP, "HighTemp control sensor");
  present(CHILD_ID_MOTION, V_TRIPPED, "Motion control Sensor");

  lastTemp = 0;
}

void loop()
{
  temp = Average_Temp_Read();
  Serial.print("HighTemp Value: ");
  Serial.print(temp);
  Serial.println(" C");

  if(temp > 150)
  {
     Serial.println("Wow it's hot today!");
  }
  else if(temp > 200)
  {
    Serial.println("Alarm! It's going to start burning!");
  }
/*  // to send string value use:
  char buf[20];
  strcpy (buf,"Hello ");
  strcat (buf,"world");
  strcat (buf,"!");
or 
char buf[20];
sprintf(buf, "%d.%d", Alarm1_Time_Local[0], Alarm1_Time_Local[1]);
send(MySensors_MSG_Alarm1_Time.set(buf), true);
*/
  if ((1==1) || (temp != lastTemp)) {
    send(msg_TEMP.set(temp));
    lastTemp = temp;
  }
  sleep(SLEEP_TIME); //sleep for: sleepTime
}

float Average_Temp_Read()
{
  int i;
  float rs=0;

  for (i=0; i<READ_SAMPLE_TIMES; i++) {
    rs += readThermocouple();
    delay(READ_SAMPLE_INTERVAL);
  }

  rs = rs/READ_SAMPLE_TIMES;

  return rs;
}

uint16_t readThermocouple1() {
  return 1;
}

double readThermocouple() {

  uint16_t v;
  pinMode(MAX6675_CS, OUTPUT);
  pinMode(MAX6675_SO, INPUT);
  pinMode(MAX6675_SCK, OUTPUT);
  
  digitalWrite(MAX6675_CS, LOW);
  delay(1);

  // Read in 16 bits,
  //  15    = 0 always
  //  14..2 = 0.25 degree counts MSB First
  //  2     = 1 if thermocouple is open circuit  
  //  1..0  = uninteresting status
  
  v = shiftIn(MAX6675_SO, MAX6675_SCK, MSBFIRST);
  v <<= 8;
  v |= shiftIn(MAX6675_SO, MAX6675_SCK, MSBFIRST);
  
  digitalWrite(MAX6675_CS, HIGH);
  if (v & 0x4) 
  {    
    // Bit 2 indicates if the thermocouple is disconnected
    return NAN;     
  }

  // The lower three bits (0,1,2) are discarded status bits
  v >>= 3;

  // The remaining bits are the number of 0.25 degree (C) counts
  return v*0.25;
}
