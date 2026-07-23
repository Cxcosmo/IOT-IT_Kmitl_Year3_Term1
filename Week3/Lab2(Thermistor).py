import time
import spidev
import math

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

VREF = 3.3
R_FIXED = 10000.0

R0 = 10000.0
T0 = 298.15
BETA = 3950.0

def ReadChannel(channel):
    adc = spi.xfer2([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data

def adc_to_voltage(reading):
    return (reading / 4095.0) * VREF

def voltage_to_resistance(vout):
    if vout <= 0:
        return None
    return R_FIXED * vout / (VREF - vout)

def resistance_to_temperature(r_thermistor):
    if r_thermistor is None or r_thermistor <= 0:
        return None
    inv_T = (1.0 / T0) + (1.0 / BETA) * math.log(r_thermistor / R0)
    T_kelvin = 1.0 / inv_T
    T_celsius = T_kelvin - 273.15
    return T_celsius

while True:
    reading = ReadChannel(0)
    vout = adc_to_voltage(reading)
    r_th = voltage_to_resistance(vout)
    temp_c = resistance_to_temperature(r_th)

    if temp_c is not None:
        print("ADC=%d\tV=%.3f\tR=%.1f\tTemp=%.2f C" % (reading, vout, r_th, temp_c))
    else:
        print("ADC=%d\tV=%.3f\t(อ่านค่าไม่ได้)" % (reading, vout))

    time.sleep(1)
