import usb.core
import usb.util
import time

# find the device
dev = usb.core.find(idVendor=0x1a86, idProduct=0x7584)

# if the device is not found, raise an exception
if dev is None:
    raise ValueError('Device not found')

# set the active configuration
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
interface_number = cfg[(0,0)].bInterfaceNumber
alternate_setting = usb.control.get_interface(dev, interface_number)
intf = usb.util.find_descriptor(
    cfg, bInterfaceNumber=interface_number,
    bAlternateSetting=alternate_setting
)
ep = usb.util.find_descriptor(
    intf,
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
)

f = open("file.txt", "rt")
text = f.read()
text = text.splitlines( keepends=True)

# send data to the device
ep.write(b'\x1B\x40')
ep.write(b'\x1B\x52\x00')
ep.write(b'\x1B\x74\x01')
ep.write(b'\x1B\x36\x12')
ep.write(b'\x1B\x50')
ep.write(b'\x1B\x70\x00')
for t in text:
    ep.write(bytes(t, 'utf-8'))
    time.sleep(0.5)
