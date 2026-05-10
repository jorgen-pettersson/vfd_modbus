#!/usr/bin/env python3
import argparse
import logging
import time
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VFDTestController:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, slave_id=1, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.slave_id = slave_id
        self.timeout = timeout
        self.client = None
        
        self.REG_CONTROL = 0x2000
        self.REG_SPEED = 0x1000
        self.REG_STATUS = 0x3000
        self.REG_FAULT_CODE = 0x8000
        self.REG_COMM_FAULT = 0x8001
        
        self.CMD_RUN_FORWARD = 1
        self.CMD_RUN_REVERSE = 2
        self.CMD_COAST_STOP = 5
        self.CMD_RAMP_STOP = 6
        self.CMD_FAULT_RESET = 7
    
    def connect(self):
        try:
            self.client = ModbusSerialClient(
                port=self.port,
                baudrate=self.baudrate,
                parity="N",
                stopbits=1,
                bytesize=8,
                timeout=self.timeout,
            )
            
            if not self.client.connect():
                logger.error(f"Failed to connect to {self.port}")
                return False
            
            logger.info(f"Connected to VFD on {self.port} at {self.baudrate} baud (Slave ID: {self.slave_id})")
            return True
            
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Disconnected from VFD")
    
    def _write_register(self, address, value):
        try:
            result = self.client.write_register(address, value, device_id=self.slave_id)
            if result.isError():
                logger.error(f"Write failed at 0x{address:04X}: {result}")
                return False
            logger.info(f"Write successful: 0x{address:04X} = {value}")
            return True
        except ModbusException as e:
            logger.error(f"Modbus error writing 0x{address:04X}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error writing: {e}")
            return False
    
    def _read_register(self, address):
        try:
            result = self.client.read_holding_registers(address, count=1, device_id=self.slave_id)
            if result.isError():
                logger.error(f"Read failed at 0x{address:04X}: {result}")
                return None
            value = result.registers[0]
            logger.info(f"Read successful: 0x{address:04X} = {value}")
            return value
        except ModbusException as e:
            logger.error(f"Modbus error reading 0x{address:04X}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error reading: {e}")
            return None
    
    def set_speed_percent(self, percent):
        if percent < 0 or percent > 100:
            logger.error(f"Invalid speed percentage: {percent}. Must be 0-100.")
            return False
        
        frequency_value = int((percent / 100) * 10000)
        return self._write_register(self.REG_SPEED, frequency_value)
    
    def set_frequency_hz(self, hz):
        if hz < 0 or hz > 50:
            logger.error(f"Invalid frequency: {hz}Hz. Must be 0-50Hz.")
            return False
        
        frequency_value = int((hz / 50) * 10000)
        return self._write_register(self.REG_SPEED, frequency_value)
    
    def start_forward(self, speed_percent=None):
        logger.info("Starting VFD in FORWARD direction")
        
        if speed_percent is not None:
            if not self.set_speed_percent(speed_percent):
                return False
            time.sleep(0.1)
        
        return self._write_register(self.REG_CONTROL, self.CMD_RUN_FORWARD)
    
    def start_reverse(self, speed_percent=None):
        logger.info("Starting VFD in REVERSE direction")
        
        if speed_percent is not None:
            if not self.set_speed_percent(speed_percent):
                return False
            time.sleep(0.1)
        
        return self._write_register(self.REG_CONTROL, self.CMD_RUN_REVERSE)
    
    def coast_stop(self):
        logger.info("Coast STOP (immediate)")
        return self._write_register(self.REG_CONTROL, self.CMD_COAST_STOP)
    
    def ramp_stop(self):
        logger.info("Ramp STOP (deceleration)")
        return self._write_register(self.REG_CONTROL, self.CMD_RAMP_STOP)
    
    def fault_reset(self):
        logger.info("FAULT RESET")
        return self._write_register(self.REG_CONTROL, self.CMD_FAULT_RESET)
    
    def emergency_stop(self):
        logger.warning("EMERGENCY STOP")
        return self.coast_stop()
    
    def get_status(self):
        status = self._read_register(self.REG_STATUS)
        if status is None:
            return None
        
        status_info = {
            'raw': status,
            'running': bool(status & 0x0001),
            'reverse': bool(status & 0x0002),
            'fault': bool(status & 0x0004)
        }
        
        logger.info(f"Status: Running={status_info['running']}, "
                   f"Reverse={status_info['reverse']}, Fault={status_info['fault']}")
        return status_info
    
    def is_running(self):
        status = self.get_status()
        if status:
            return status['running']
        return None
    
    def has_fault(self):
        status = self.get_status()
        if status:
            return status['fault']
        return None
    
    def get_fault_code(self):
        fault_code = self._read_register(self.REG_FAULT_CODE)
        if fault_code and fault_code > 0:
            logger.warning(f"Fault code: {fault_code}")
        return fault_code
    
    def get_comm_fault(self):
        return self._read_register(self.REG_COMM_FAULT)

def main():
    parser = argparse.ArgumentParser(description='Test basic VFD commands')
    parser.add_argument('--port', default='/dev/ttyUSB0', help='Serial port')
    parser.add_argument('--baudrate', type=int, default=9600, help='Baud rate')
    parser.add_argument('--slave', type=int, default=1, help='Modbus slave ID')
    parser.add_argument('--status', action='store_true', help='Read status only')
    args = parser.parse_args()
    
    controller = VFDTestController(args.port, args.baudrate, args.slave)
    
    try:
        if not controller.connect():
            return 1
        
        if args.status:
            controller.get_status()
            controller.get_fault_code()
            return 0
        
        print("\nVFD Test Controller - Ready for commands")
        print("Available methods:")
        print("  .start_forward([speed])  - Start forward (0-100% speed)")
        print("  .start_reverse([speed])  - Start reverse (0-100% speed)")
        print("  .ramp_stop()             - Stop with deceleration")
        print("  .coast_stop()            - Immediate stop")
        print("  .fault_reset()           - Reset VFD faults")
        print("  .set_speed_percent(p)    - Set speed (0-100%)")
        print("  .set_frequency_hz(hz)    - Set frequency (0-50Hz)")
        print("  .get_status()            - Read current status")
        print("  .is_running()            - Check if running")
        print("  .has_fault()             - Check for faults")
        print("\nExample:")
        print("  controller.start_forward(25)")
        print("  controller.get_status()")
        print("  controller.ramp_stop()")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        return 0
    finally:
        controller.disconnect()

if __name__ == "__main__":
    import sys
    sys.exit(main())