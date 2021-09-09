#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

WiFiServer server(80);

const char *ssid = "ESP8266 AP YK";
const char *password = "justpassword";

void setup() {
  delay(10000);
  Serial.begin(9600);
  //Serial.println('\n');
  WiFi.mode(WIFI_AP);
  WiFi.setSleepMode(WIFI_NONE_SLEEP);
  WiFi.softAP(ssid, password);

  //Serial.println("Access Point started");

  //Serial.println(WiFi.softAPIP());
  
  server.begin();
  //Serial.println("Server started");
}

void loop() {
  WiFiClient client = server.available();
  if(client){
    //Serial.println("Client connected");
    while(client.connected()){
      
      while(client.available()>0){
        char c = client.read();
        Serial.write(c);
      }

      while(Serial.available()>0){
        char c = Serial.read();
        client.write(c);
      }
      
      delay(10); 
    }
    
    client.stop();
    //Serial.println("Client disconnected");
  }

}
