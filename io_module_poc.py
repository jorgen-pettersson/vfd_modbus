import threading

from pymodbus.client import ModbusSerialClient
import time
from command_queue import set_output, get_inputs,modbus_worker


def callback_on_input_change(inputs):
    print("Input changed: "+str(inputs))

def monitor_inputs(target = None):
    previous_inputs = None
    while True:
        inputs = get_inputs("io_1")

        if previous_inputs is not None and len(previous_inputs) == len(inputs) and inputs != previous_inputs:
            target(inputs)
        #target(inputs)
        previous_inputs = inputs

        time.sleep(1)

def main():
    print("Starting IO module PoC...")

    client = ModbusSerialClient(
        port="/dev/ttyUSB0",   # Windows example: COM3
        baudrate=9600,
        parity='N',
        stopbits=1,
        bytesize=8,
        timeout=1
    )

    client.connect()

    SLAVE_ID = 1

    print("First step done, now testing command queue...")
    # modbus_worker(client, device_id=SLAVE_ID)
    worker_thread = threading.Thread(
        target=modbus_worker,
        args=(client,),
        daemon=True
    )

    worker_thread.start()
    print("worker thread started")

    set_output(SLAVE_ID,0, True)
    print("DO_01 ON via command queue")

    monitor_inputs(target=callback_on_input_change)

    client.close()

# -----------------------------------------------
if __name__ == "__main__":
    import sys
    sys.exit(main())