import asyncio

from aiocoap import Context, Message
import aiocoap

import RPi.GPIO as GPIO


# =========================
# CoAP Server
# =========================

SERVER_IP = "10.210.23.224"
SERVER_PORT = 5683


# =========================
# LED
# =========================

LED_PIN = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

pwm = GPIO.PWM(LED_PIN, 1000)
pwm.start(0)


# =========================
# รับค่าจาก Observe
# =========================

def handle_observe(response):

    try:

        # Arduino ส่งมาเป็น เช่น b"2.35"
        voltage = float(response.payload.decode())

        # 0 - 5V
        # แปลงเป็น 0 - 100%
        duty = (voltage / 5.0) * 100

        # ป้องกันค่าหลุดช่วง
        duty = max(0, min(100, duty))

        # ปรับความสว่าง LED
        pwm.ChangeDutyCycle(duty)

        print(
            "Voltage = {:.2f} V | Brightness = {:.1f}%".format(
                voltage,
                duty
            )
        )

    except Exception as e:

        print("Error:", e)


# =========================
# Observe
# =========================

async def observe_pot():

    protocol = await Context.create_client_context()

    request = Message(
        code=aiocoap.Code.GET,
        uri=f"coap://{SERVER_IP}:{SERVER_PORT}/pot"
    )

    request.opt.observe = 0

    requester = protocol.request(request)

    requester.observation.register_callback(
        handle_observe
    )

    response = await requester.response

    print("Observe started")
    print("Code:", response.code)

    while True:
        await asyncio.sleep(1)


# =========================
# Main
# =========================

async def main():

    try:

        await observe_pot()

    finally:

        pwm.stop()
        GPIO.cleanup()


asyncio.run(main())
