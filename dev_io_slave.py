from pymodbus.server import StartSerialServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusDeviceContext,
    ModbusServerContext,
)

DEVICE_ID = 2
SERIAL_PORT = "/dev/serial0"   # or /dev/serial0, depending on your Pi/HAT

def main():
    print("Starting IO module PoC...")
    #
    # Data areas:
    # di = discrete inputs   read_discrete_inputs()
    # co = coils             read_coils() / write_coil()
    # hr = holding registers read/write registers
    # ir = input registers   read input registers
    device_context = ModbusDeviceContext(
        di=ModbusSequentialDataBlock(0, [0] * 100),
        co=ModbusSequentialDataBlock(0, [0] * 100),
        hr=ModbusSequentialDataBlock(0, [0] * 100),
        ir=ModbusSequentialDataBlock(0, [0] * 100),
    )

    context = ModbusServerContext(
        devices={DEVICE_ID: device_context},
        single=False,
    )

    # Example initial fake input states
    # DI_01 = True, DI_02 = False, DI_03 = True
    device_context.setValues(2, 0, [1, 0, 1, 0, 0, 0, 0, 0])

    print(f"Starting fake Modbus RTU slave on {SERIAL_PORT}, device_id={DEVICE_ID}")

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