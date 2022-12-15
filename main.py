import serial
import time

# z1baudrate = 9600
# z1port = '/dev/cu.usbmodem141101'  # set the correct port before run it
#
# z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
# z1serial.timeout = 2  # set read timeout
# print(z1serial) # debug serial.
# print(z1serial.is_open)  # True if open
# if z1serial.is_open:
#     while True:
#         size = z1serial.inWaiting()
#         if size:
#             data = z1serial.read(size)
#             print(data)
#         # else:
#         #     print('no data')
#         time.sleep(1)
# else:
#     print('z1serial not open')
# z1serial.close()  # close z1serial if z1serial is open.


import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
    print("{}".format(port))