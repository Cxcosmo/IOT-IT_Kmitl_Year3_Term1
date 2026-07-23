from RPLCD. i2c import CharLCD
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

lcd.write_string("Hello, Raspberry")
lcd.crlf()
lcd.write_string("I2C LCD Ready!")

time.sleep(5)

lcd.clear()
lcd.write_string("Line 1 Example")
lcd.crlf()
lcd.write_string("Temp: 25.5 C")
