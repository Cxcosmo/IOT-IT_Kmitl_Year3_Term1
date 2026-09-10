import asyncio

from aiocoap import resource, Context, Message
import aiocoap
import RPi.GPIO as GPIO

LIGHT = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT, GPIO.OUT)

pwm = GPIO.PWM(LIGHT, 100)
pwm.start(0)


class TemperatureResource(resource.Resource):

    async def render_get(self, request):

        print("Method:", request.code)
        print("Payload:", request.payload)
        print("GET /temperature")

        temperature = "25.6"

        return Message(
            code=aiocoap.Code.CONTENT,
            payload=temperature.encode()
        )


class LEDResource(resource.Resource):

    async def render_put(self, request):

        print("Method:", request.code)
        print("Payload:", request.payload)

        try:
            # แปลง Payload จาก bytes -> string -> int
            brightness = int(request.payload.decode())

            print("PUT /led =", brightness)

            # จำกัดค่าให้อยู่ระหว่าง 0-100
            brightness = max(0, min(100, brightness))

            # ปรับความสว่าง LED
            pwm.ChangeDutyCycle(brightness)

            print("LED Brightness:", brightness, "%")

            return Message(
                code=aiocoap.Code.CHANGED,
                payload=f"Brightness = {brightness}%".encode()
            )

        except ValueError:

            return Message(
                code=aiocoap.Code.BAD_REQUEST,
                payload=b"Payload must be a number 0-100"
            )


async def main():

    root = resource.Site()

    root.add_resource(
        ["temperature"],
        TemperatureResource()
    )

    root.add_resource(
        ["led"],
        LEDResource()
    )

    await Context.create_server_context(
        root,
        bind=("10.210.23.245", 5683)
    )

    print("CoAP Server started")
    print("Port: 5683")

    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        pwm.stop()
        GPIO.cleanup()
