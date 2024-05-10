#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <stdlib.h>

#define BUZZ_PIN 0
#define BOARD_ID "source"
#define TIME_TOPIC "offset"
#define SYNC_TOPIC "sync"

const char* ssid = "DECO_E4";
const char* password = "ADFE9625C9C271143ECEA74A53";

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long messageTime = 0;
volatile bool beep = false;
unsigned long buzzTime = 0;
unsigned long lastBuzzTime = 0;
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
  if (topic == SYNC_TOPIC) { sync = false; }
  if (topic == BOARD_ID) {
    if ((char)message[0] == '1') {
      beep = true;
    } else if ((char)message[0] == '0') {
      beep = false;
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(BOARD_ID)) {
      Serial.println("connected");  
      client.subscribe(TIME_TOPIC);
      client.subscribe(SYNC_TOPIC);
      client.subscribe(BOARD_ID);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup(void) {
  pinMode(BUZZ_PIN, OUTPUT);
  digitalWrite(BUZZ_PIN, HIGH);
  Serial.begin(115200);
  setupWifi();
  IPAddress mqtt_server(192,168,1,48);
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void buzz() {
    digitalWrite(BUZZ_PIN, LOW);
    delay(10);
    digitalWrite(BUZZ_PIN, HIGH);
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
    if (beep && micros() - lastBuzzTime > 500000) {
      buzzTime = micros();
      char buff[sizeof(unsigned long) * 8 + 1];
      ltoa(buzzTime, buff, 10);
      client.publish(BOARD_ID, buff);
      Serial.println(buff);
      lastBuzzTime = buzzTime;
      buzz();
    }
  }
}
