from pymodbus.server import StartSerialServer
from pymodbus.simulator import SimData, SimDevice, DataType

DEVICE_ID = 2
#SERIAL_PORT = "/dev/serial0"   # or /dev/serial0, depending on your Pi/HAT
SERIAL_PORT = "/dev/ttyUSB0" 

def main():
    print("Starting IO module PoC...")

    # Non-shared Modbus model:
    # tuple order = coils, discrete inputs, holding registers, input registers
    device = SimDevice(
        id=DEVICE_ID,
        simdata=(
            [SimData(address=0, count=100, values=False, datatype=DataType.BITS)],      # coils
            [SimData(address=0, count=100, values=False, datatype=DataType.BITS)],      # discrete inputs
            [SimData(address=0, count=100, values=0, datatype=DataType.REGISTERS)],     # holding registers
            [SimData(address=0, count=100, values=0, datatype=DataType.REGISTERS)],     # input registers
        ),
    )

    print(f"Starting fake Modbus RTU slave id={DEVICE_ID} on {SERIAL_PORT}")

    StartSerialServer(
        context=device,
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