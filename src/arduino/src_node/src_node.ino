#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <AsyncElegantOTA.h>
#include <PubSubClient.h>
#include <stdlib.h>

#define BUZZ_PIN 0
#define BOARD_ID "source"
#define TIME_SYNC_TOPIC "chronos"

const char* ssid = "DECO_E4";
const char* password = "ADFE9625C9C271143ECEA74A53";

WiFiClient espClient;
PubSubClient client(espClient);
AsyncWebServer server(80);

unsigned long syncTime = 0;
unsigned long buzzTime = 0;
unsigned long lastBuzzTime = 0;

void setupOTA() {
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(200, "text/plain", "ESP8266 MIC");
  });

  AsyncElegantOTA.begin(&server);    // Start ElegantOTA
  server.begin();
  Serial.println("HTTP server started");
}

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
  if (topic == TIME_SYNC_TOPIC) { syncTime = micros(); }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(BOARD_ID)) {
      Serial.println("connected");  
      client.subscribe(TIME_SYNC_TOPIC);
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
  setupOTA();
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
  if (!client.loop()) { client.connect(TIME_SYNC_TOPIC); }
  
  if (micros() - lastBuzzTime > 500000) {
    buzzTime = micros() - syncTime;
    char buff[sizeof(unsigned long) * 8 + 1];
    ltoa(buzzTime, buff, 10);
    client.publish(BOARD_ID, buff);
    Serial.println(buff);
    lastBuzzTime = micros();
    buzz();
  }
}
