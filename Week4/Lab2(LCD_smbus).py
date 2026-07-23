from RPLCD.i2c import CharLCD
from smbus3 import SMBus, i2c_msg
import time

lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
    cols=16,
    rows=2,
    dotsize=8,
    charmap='A00',
    auto_linebreaks=True,
    backlight_enabled=True
)

while True:
    with SMBus(1) as bus:
        write = i2c_msg.write(0x44, [0x2C, 0x06])
        bus.i2c_rdwr(write)

        time.sleep(0.5)

        read = i2c_msg.read(0x44, 6)
        bus.i2c_rdwr(read)

        data = list(read)

    temp = data[0] * 256 + data[1]
    cTemp = -45 + (175 * temp / 65535.0)
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

    lcd.clear()
    lcd.write_string(f"Temp:{cTemp:.2f} C")
    lcd.cursor_pos = (1, 0)
    lcd.write_string(f"Hum:{humidity:.2f}%")
    time.sleep(0.5)
