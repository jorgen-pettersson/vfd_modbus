import queue
import threading
import time

cmd_queue = queue.Queue()
#latest_inputs = [False] * 1
latest_inputs = {}
latest_lock = threading.Lock()

devices = [
    {"name": "io_1", "device_id": 1, "type": "wp8028","noOfInputs":8},
    {"name": "io_1_dev", "device_id": 2, "type": "wp8028","noOfInputs":8}
]

def modbus_worker(client):
    global latest_inputs

    while True:
        # 1. Handle pending writes first
        try:
            cmd = cmd_queue.get_nowait()
            if cmd["type"] == "write_coil":
                client.write_coil(
                    cmd["address"],
                    cmd["value"],
                    device_id=cmd["device_id"]
                )
        except queue.Empty:
            pass
        
        for device in devices:
            if device["noOfInputs"] > 0:
                result = client.read_discrete_inputs(
                    address=0,
                    count=device["noOfInputs"],
                    device_id=device["device_id"]
                )

                if not result.isError():    
                    latest_inputs[device["name"]] = result.bits[:8]


        ### TEST ABOVE WITH SINGLE DEVICE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        #result = client.read_discrete_inputs(address=0, count=8, device_id=1)
        
        #if not result.isError():
        #    with latest_lock:
        #        latest_inputs = result.bits[:8]
        #else:
        #    print(f"Error reading inputs: {result}")
            
        time.sleep(0.1)


def set_output(device_id,address, value):
    cmd_queue.put({
        "type": "write_coil",
        "device_id": device_id,
        "address": address,
        "value": value
    })


def get_inputs(device_name=None):
    with latest_lock:
        if device_name in latest_inputs:
            return list(latest_inputs[device_name])
        else:
            return list(latest_inputs)
