#include <WiFiS3.h>
#include <WiFiUdp.h>
#include <coap-simple.h>

// ===== WiFi =====
const char WIFI_SSID[] = "Net for cat";
const char WIFI_PASSWORD[] = "Cat_Only";

const uint16_t COAP_PORT = 5683;

// ===== Potentiometer =====
const int POT_PIN = A0;

WiFiUDP udp;
Coap coap(udp);


// ---------- WiFi ----------
void connectWiFi() {

  int status = WL_IDLE_STATUS;

  while (status != WL_CONNECTED) {

    Serial.print("Connecting to SSID: ");
    Serial.println(WIFI_SSID);

    status = WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    delay(5000);
  }

  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}


// ---------- GET /pot ----------
void handlePot(CoapPacket &packet, IPAddress ip, int port) {

  int raw = analogRead(POT_PIN);

  // 12-bit ADC : 0 - 4095
  float voltage = raw * 5.0 / 4095.0;

  char payload[20];

  snprintf(
    payload,
    sizeof(payload),
    "%.2f",
    voltage
  );

  // ถ้าเป็น Observe request
  uint32_t observeValue = 0;

  if (packet.getObserveValue(observeValue)) {

    // Observe = 0 -> subscribe
    if (observeValue == 0) {

      if (!coap.addObserver(
            "pot",
            ip,
            port,
            packet.token,
            packet.tokenlen
          )) {

        coap.sendResponse(
          ip,
          port,
          packet.messageid,
          "busy"
        );

        return;
      }

      // ส่งค่าแรกกลับไป
      coap.sendObserveResponse(
        ip,
        port,
        packet.messageid,
        payload,
        strlen(payload),
        COAP_CONTENT,
        COAP_TEXT_PLAIN,
        packet.token,
        packet.tokenlen,
        0
      );

      Serial.println("Raspberry Pi subscribed to /pot");
    }

    // Observe = 1 -> unsubscribe
    else if (observeValue == 1) {

      coap.removeObserver(
        "pot",
        ip,
        port,
        packet.token,
        packet.tokenlen
      );

      coap.sendResponse(
        ip,
        port,
        packet.messageid,
        "unsubscribed"
      );
    }

  } else {

    // GET ธรรมดา
    coap.sendResponse(
      ip,
      port,
      packet.messageid,
      payload
    );
  }
}


// ---------- Setup ----------
void setup() {

  Serial.begin(115200);

  // UNO R4 สามารถใช้ 12-bit ADC
  analogReadResolution(12);

  connectWiFi();

  udp.begin(COAP_PORT);

  // Resource
  coap.server(handlePot, "pot");

  coap.start();

  Serial.println();
  Serial.println("CoAP Server Ready");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("Resource: /pot");
}


// ---------- Loop ----------
void loop() {

  coap.loop();

  // อ่าน potentiometer
  static int lastRaw = -1;

  int raw = analogRead(POT_PIN);

  // ถ้าค่าเปลี่ยน ค่อยแจ้ง Observer
  if (raw != lastRaw) {

    lastRaw = raw;

    float voltage = raw * 5.0 / 4095.0;

    char payload[20];

    snprintf(
      payload,
      sizeof(payload),
      "%.2f",
      voltage
    );

    Serial.print("Voltage: ");
    Serial.println(payload);

    // ส่ง notification ไปยัง client ที่ Observe อยู่
    coap.notify(
      "pot",
      payload,
      strlen(payload),
      COAP_TEXT_PLAIN
    );
  }

  delay(50);
}