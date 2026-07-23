from RPLCD. i2c import CharLCD
import smbus3
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

bus = smbus3. SMBus (1)

bus.i2c_wr(0x44,[0x2C,0x06])
time.sleep(0.5)

msg = bus.i2c_rd(0x44, 6)
data = bytes(msg)
bus.close

temp = data[0] * 256 + data[1]
cTemp = -45 + (175 * temp / 65535.0)
humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

lcd.write_string(f"Temperature in Celsius is : {cTemp:.2f}C")
lcd.crlf()
lcd.write_string(f"Relative Humidity is : {humidity:.2f} RH")

