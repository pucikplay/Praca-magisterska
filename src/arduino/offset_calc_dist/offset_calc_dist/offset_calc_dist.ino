#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <stdlib.h>

#define MIC_PIN 0
#define BOARD_ID "0"
#define TIME_TOPIC "offset"
#define TOPIC "sync"

const char* ssid = "DECO_E4";
const char* password = "ADFE9625C9C271143ECEA74A53";

WiFiClient espClient;
PubSubClient client(espClient);

volatile bool active = false;
volatile bool micInput = false;
unsigned long micTime = 0;
unsigned long lastMicTime = 0;
unsigned long currTime = 0;
unsigned long messageTime = 0;
bool sync = true;

void setupWifi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(String topic, byte* message, unsigned int length) {
//  Serial.print("Message arrived on topic: ");
//  Serial.print(topic);
//  Serial.print(". Message: ");
//  String messageTemp;
  
//  for (int i = 0; i < length; i++) {
//    Serial.print((char)message[i]);
//    messageTemp += (char)message[i];
//  }
//  Serial.println();
  if (topic == TIME_TOPIC) { messageTime = micros(); }
  if (topic == TOPIC) {sync = false; }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(BOARD_ID)) {
      Serial.println("connected");  
      client.subscribe(TIME_TOPIC);
      client.subscribe(TOPIC);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void ICACHE_RAM_ATTR mic_rising() {
  currTime = micros();
  if (currTime - lastMicTime > 200000) {
    lastMicTime = currTime;
    micInput = true;
  }
}

void setup(void) {
  pinMode(MIC_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(MIC_PIN), mic_rising, RISING);
  Serial.begin(115200);
  setupWifi();
  IPAddress mqtt_server(192,168,1,48);
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) { reconnect(); }
  if (!client.loop()) { client.connect(TIME_TOPIC); }
  
  if (sync) {
    if (messageTime != 0) {
      if (micros() - messageTime > 100000) {
        char T1[sizeof(unsigned long) * 8 + 1];
        ltoa(messageTime, T1, 10);
        char T2[sizeof(unsigned long) * 8 + 1];
        ltoa(micros(), T2, 10);
        char mssg[strlen(T1) + strlen(T2) + 2];
        strcpy(mssg, T1);
        strcat(mssg, " ");
        strcat(mssg, T2);
        client.publish(BOARD_ID, mssg);
        Serial.println(mssg);
        messageTime = 0;
      }
    }
  }
  else {
    if (micInput == true) {
      char mssg[sizeof(unsigned long) * 8 + 1];
      ltoa(lastMicTime, mssg, 10);
      client.publish(BOARD_ID, mssg);
      Serial.println(mssg);
      micInput = false;
    }
  }
}
