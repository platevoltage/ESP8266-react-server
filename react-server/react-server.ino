

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include "FS.h"

#include "payload/index.html.h"
#include "payload/manifest.json.h"
#include "payload/static/js/main.32002a2b.js.h"
#include "payload/static/js/787.05b7a068.chunk.js.h"
#include "payload/static/css/main.f8f8c452.css.h"
// #include "payload/static/css/main.f8f8c452.css.map.h"


#ifndef STASSID
#define STASSID "Can't stop the signal, Mal"
#define STAPSK  "youcanttaketheskyfromme"
#endif

const char *ssid = STASSID;
const char *password = STAPSK;

ESP8266WebServer server(80);

void sendFile(String fileName, String fileType) {
  File testFile = SPIFFS.open(fileName, "r");
  if (!testFile) {
    Serial.println("file open failed");
    Serial.println(fileName);
  }
  server.setContentLength(CONTENT_LENGTH_UNKNOWN);
  server.send(200, fileType, "" );
    while(testFile.available()) 
    {
      //read line by line from the file
      String line;
      if (fileType == "text/javascript" || fileType == "text/json") {
        line = testFile.readStringUntil(' ');
        if (line != "") server.sendContent(line + " ");
      }
      else {
        line = testFile.readStringUntil('\n');
        if (line != "") server.sendContent(line);
      } 
      
      // server.send(200, "text/html", line);
      
    }
    server.client().stop();
    Serial.println("Done");
}


void handleRoot() {

  // sendFile("/index.html", "text/html");
  server.send(200, "text/html", _index_html);

  
}

void handleJS() {
  // sendFile("/static/js/main.js", "text/javascript");
  server.send(200, "text/javascript", _main_js);
}
void handleCSS() {
  // sendFile("/static/css/main.f8f8c452.css", "text/css");
  server.send(200, "text/css", _main_css);
}
// void handleCSSMap() {

//   server.send(200, "text/json", _main_css_map);
// }
void handleJSChunk() {
  // sendFile("/static/css/main.css.map", "text/json");
  server.send(200, "text/javascript", _chunk_js);
}
void handleManifest() {
  // sendFile("/manifest.json", "text/json");
  server.send(200, "text/json", _manifest_json);
}

void handleNotFound() {
  digitalWrite(LED_BUILTIN, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";

  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }

  server.send(404, "text/plain", message);
  digitalWrite(LED_BUILTIN, 0);
}


void turnOn() {
  server.send(200, "text/json", "{ \"led\":\"on\" }");
  digitalWrite(LED_BUILTIN, 0);
  Serial.println("led on");
}

void turnOff() {
  server.send(200, "text/json", "{ \"led\":\"off\" }");
  digitalWrite(LED_BUILTIN, 1);
  Serial.println("led off");
  ///fsdfdfsdfsdsdfsssssss
}



void setup(void) {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, 0);
  Serial.begin(9600);
  bool result = SPIFFS.begin();
  Serial.println("SPIFFS opened: " + result);
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

  if (MDNS.begin("test")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", [](){ server.send(200, "text/html", _index_html); });

  server.on("/RGB-strip-controller/static/js/main.32002a2b.js", handleJS);
  server.on("/RGB-strip-controller/static/js/main.32002a2b.js.map", handleJSChunk);
  server.on("/RGB-strip-controller/static/css/main.f8f8c452.css", handleCSS);
  // server.on("/RGB-strip-controller/static/css/main.f8f8c452.css.map", handleCSSMap);
  server.on("/RGB-strip-controller/manifest.json", handleManifest);
  server.on("/on", turnOn);
  server.on("/off", turnOff);
  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();
}

