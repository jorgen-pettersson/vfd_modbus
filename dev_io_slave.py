from pymodbus.server import StartSerialServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusDeviceContext,
    ModbusServerContext,
)

DEVICE_ID = 2
SERIAL_PORT = "/dev/serial0"   # or /dev/serial0, depending on your Pi/HAT
#SERIAL_PORT = "/dev/ttyUSB0" 

def main():
    print("Starting IO module PoC...")

    di_block = ModbusSequentialDataBlock(1, [1, 0, 1, 0, 0, 0, 0, 0] + [0] * 92)
    co_block = ModbusSequentialDataBlock(1, [0] * 100)
    hr_block = ModbusSequentialDataBlock(1, [0] * 100)
    ir_block = ModbusSequentialDataBlock(1, [0] * 100)

    device_context = ModbusDeviceContext(
        di=di_block,
        co=co_block,
        hr=hr_block,
        ir=ir_block,
    )

    context = ModbusServerContext(
        devices={DEVICE_ID: device_context},
        single=False,
    )

    print(f"Starting fake slave device_id={DEVICE_ID} on {SERIAL_PORT}")

    StartSerialServer(
        context=context,
        port=SERIAL_PORT,
        baudrate=9600,
        parity="N",
        stopbits=1,
        bytesize=8,
    )

    
# -----------------------------------------------
if __name__ == "__main__":
    import sys
    sys.exit(main())