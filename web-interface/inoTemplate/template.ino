#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

//----begin generated includes and wifi definitions

//XXX

//----end generated includes and wifi definitions


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
      
      
    }
    server.client().stop();
    Serial.println("Done");
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

  //-----begin generated paths

  //XXX

  //-----end generated paths
  
  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();
}

