import time
import spidev

spi = spidev.SpiDev() # Open SPI bus
spi.open(0, 0)
spi.max_speed_hz = 500000

def ReadChannel(channel): # read channel (0-7) from MCP3208
    adc = spi.xfer2([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data

while True:
    reading = ReadChannel(0)
    percent = 100 - (reading * 100 / 3700)
    print("Reading=%d\t Voltage=%f" % (reading, percent))
    time.sleep(1)

