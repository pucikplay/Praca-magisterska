#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <stdlib.h>

#define BOARD_ID "3"
#define TOPIC "synch"
#define NO_MESSAGES 100
#define PAUSE 50000

const char* ssid = "DECO_E4";
const char* password = "ADFE9625C9C271143ECEA74A53";

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long messageTime = 0;
unsigned long iter = 0;

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
  if (topic == TOPIC) {
    messageTime = micros();
    Serial.printf("messageTime: %ld", messageTime);
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(BOARD_ID)) {
      Serial.println("connected");
      Serial.printf("BOARD_ID: %s\n", BOARD_ID);
      client.subscribe(TOPIC);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup(void) {
  Serial.begin(115200);
  setupWifi();
  IPAddress mqtt_server(192,168,1,48);
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) { reconnect(); }
  if (!client.loop()) { client.connect(TOPIC); }
  
  if (messageTime != 0 && iter < NO_MESSAGES) {
    if (micros() - messageTime > PAUSE * (iter+1)) {
      char T1[sizeof(unsigned long) * 8 + 1];
      ltoa(iter, T1, 10);
      char T2[sizeof(unsigned long) * 8 + 1];
      ltoa((micros() - messageTime), T2, 10);
      char mssg[strlen(T1) + strlen(T2) + 2];
      strcpy(mssg, T1);
      strcat(mssg, " ");
      strcat(mssg, T2);
      client.publish(BOARD_ID, mssg);
      Serial.println(mssg);
      iter++;
    }
  }
  else {
    messageTime = 0;
    iter = 0;
  }
}
