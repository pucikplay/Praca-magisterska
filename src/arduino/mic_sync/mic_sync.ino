#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <stdlib.h>

#define MIC_PIN 0
#define BOARD_ID "0"
#define TOPIC "active"

const char* ssid = "DECO_E4";
const char* password = "ADFE9625C9C271143ECEA74A53";

WiFiClient espClient;
PubSubClient client(espClient);

volatile bool active = false;
volatile bool micInput = false;
unsigned long micTime = 0;
unsigned long lastMicTime = 0;
unsigned long currTime = 0;

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
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
    
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();
  if (topic == TOPIC && (char)message[0] == BOARD_ID[0]) {
    active = !active;
    Serial.printf("Active is %d\n", active);
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
  if (!client.loop()) { client.connect(TOPIC); }
  
  if (active && micInput == true) {
    char mssg[sizeof(unsigned long) * 8 + 1];
    ltoa(lastMicTime, mssg, 10);
    client.publish(BOARD_ID, mssg);
    Serial.println(mssg);
    micInput = false;
  }
}
