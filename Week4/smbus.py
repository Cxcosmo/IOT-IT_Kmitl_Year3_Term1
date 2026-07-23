from smbus3 import SMBus, i2c_msg
import time

with SMBus(1) as bus:

    # ส่งคำสั่งวัด
    write = i2c_msg.write(0x44, [0x2C, 0x06])
    bus.i2c_rdwr(write)

    time.sleep(0.5)

    # อ่านข้อมูล 6 ไบต์
    read = i2c_msg.read(0x44, 6)
    bus.i2c_rdwr(read)

    data = list(read)

temp = data[0] * 256 + data[1]
cTemp = -45 + (175 * temp / 65535.0)
humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

print("Temperature: %.2f C" % cTemp)
print("Humidity: %.2f %%RH" % humidity)
