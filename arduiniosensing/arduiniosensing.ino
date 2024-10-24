#include <WiFi.h>
#include <HTTPClient.h>

#define FLOW_SENSOR_1_PIN 13 // GPIO for Flow Sensor 1
#define FLOW_SENSOR_2_PIN 15 // GPIO for Flow Sensor 2

// Wi-Fi credentials
const char* ssid = "GANESH";
const char* password = "12345678";

// Supabase credentials
String API_URL = "https://bolsgescbuufddyjwxqb.supabase.co/rest/v1/maintable";
String API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvbHNnZXNjYnV1ZmRkeWp3eHFiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjg4MTAwNzIsImV4cCI6MjA0NDM4NjA3Mn0.AL-ESq9iKFceAtaActhElvxPzkU6VFQ40IVdANWubEU";

// Telegram credentials
String botToken = "7561146234:AAG9eNEXSgYLmMABBWiwQD_oTHaNTEzANvQ";
String chatID = "8100295483";  // Replace with your chat ID

// Flow sensor data
volatile int flowPulse1 = 0; 
volatile int flowPulse2 = 0; 
float flowRate1 = 0.0; 
float flowRate2 = 0.0;
float flowDiff = 0.0;

// Sending interval (2 minutes)
unsigned long interval = 5000; 
unsigned long previousMillis = 0;

// Flow sensor pulse handler
void IRAM_ATTR pulseCounter1() { flowPulse1++; }
void IRAM_ATTR pulseCounter2() { flowPulse2++; }

void setup() {
  Serial.begin(115200);

  // Configure flow sensors
  pinMode(FLOW_SENSOR_1_PIN, INPUT_PULLUP);
  pinMode(FLOW_SENSOR_2_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(FLOW_SENSOR_1_PIN), pulseCounter1, FALLING);
  attachInterrupt(digitalPinToInterrupt(FLOW_SENSOR_2_PIN), pulseCounter2, FALLING);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected!");
}

void sendTelegramAlert(String message) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient https;
    String telegramUrl = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + chatID + "&text=" + message;
    
    https.begin(telegramUrl);
    int httpResponseCode = https.GET();
    
    if (httpResponseCode > 0) {
      String response = https.getString();
      Serial.println("Telegram message sent successfully.");
      Serial.println(response);
    } else {
      Serial.print("Error sending message to Telegram: ");
      Serial.println(httpResponseCode);
    }
    
    https.end();
  } else {
    Serial.println("WiFi Disconnected. Cannot send Telegram alert.");
  }
}

void loop() {
  unsigned long currentMillis = millis();
  
  // Calculate and send data every 2 minutes
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // Disable interrupts to calculate flow rates
    detachInterrupt(digitalPinToInterrupt(FLOW_SENSOR_1_PIN));
    detachInterrupt(digitalPinToInterrupt(FLOW_SENSOR_2_PIN));

    // Convert pulse count to flow rate (example conversion, modify based on your sensor)
    flowRate1 = (flowPulse1 / 7.5); // Example conversion factor for flow sensor 1
    flowRate2 = (flowPulse2 / 7.5); // Example conversion factor for flow sensor 2

    // Calculate flow rate difference
    flowDiff = flowRate1 - flowRate2;

    // Reset pulse counts
    flowPulse1 = 0;
    flowPulse2 = 0;

    // Re-enable interrupts
    attachInterrupt(digitalPinToInterrupt(FLOW_SENSOR_1_PIN), pulseCounter1, FALLING);
    attachInterrupt(digitalPinToInterrupt(FLOW_SENSOR_2_PIN), pulseCounter2, FALLING);

    // Only send data if flowRate1 is not 0
    if (flowRate1 != 0 ) {
      // Send data to database
      if (WiFi.status() == WL_CONNECTED) {
        HTTPClient https;
        https.begin(API_URL);
        https.addHeader("Content-Type", "application/json");
        https.addHeader("apikey", API_KEY);
        https.addHeader("Authorization", "Bearer " + API_KEY);

        // Create JSON payload with flow rates and difference
        String jsonData = "{\"flow_rate_1\":" + String(flowRate1) + 
                          ",\"flow_rate_2\":" + String(flowRate2) + 
                          ",\"flow_diff\":" + String(flowDiff) + "}";

        int httpResponseCode = https.POST(jsonData);

        // Print response and status
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        Serial.print("Response: ");
        Serial.println(https.getString());

        https.end();  // End the HTTPS connection
      } else {
        Serial.println("WiFi Disconnected. Cannot send data.");
      }

      // Check if flowRate1 > 1 and flowDiff > 20, send Telegram alert
      if (flowRate1 > 1 && flowDiff > 20 ) {
        String alertMessage = "Alert🚨🚨: Flow rate 1 is " + String(flowRate1) + 
                              " and the difference between the flow rates is " + String(flowDiff);
        sendTelegramAlert(alertMessage);
      }

    } else {
      Serial.println("Flow Rate 1 is 0, data not sent.");
    }
  }
}
