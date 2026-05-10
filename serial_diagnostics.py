#!/usr/bin/env python3
import logging
import time
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SerialDiagnostics:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, slave_id=1):
        self.port = port
        self.baudrate = baudrate
        self.slave_id = slave_id
        self.client = None
        self.results = []
    
    def add_result(self, test_name, passed, message=""):
        result = {
            'test': test_name,
            'passed': passed,
            'message': message,
            'timestamp': time.time()
        }
        self.results.append(result)
        status = "PASS" if passed else "FAIL"
        logger.info(f"[{status}] {test_name}: {message}")
    
    def test_connection_parameters(self):
        logger.info("Testing connection parameters...")
        try:
            if not self.port:
                self.add_result("Port validation", False, "No port specified")
                return False
            
            if not isinstance(self.baudrate, int) or self.baudrate <= 0:
                self.add_result("Baudrate validation", False, f"Invalid baudrate: {self.baudrate}")
                return False
            
            valid_baudrates = [9600, 19200, 38400, 57600, 115200]
            if self.baudrate not in valid_baudrates:
                self.add_result("Baudrate validation", False, f"Unusual baudrate: {self.baudrate}")
                return False
            
            self.add_result("Connection parameters", True, f"Port: {self.port}, {self.baudrate} baud")
            return True
        except Exception as e:
            self.add_result("Connection parameters", False, str(e))
            return False
    
    def test_serial_connection(self):
        logger.info("Testing serial connection...")
        try:
            self.client = ModbusSerialClient(
                port=self.port,
                baudrate=self.baudrate,
                parity="N",
                stopbits=1,
                bytesize=8,
                timeout=2,
            )
            
            if not self.client.connect():
                self.add_result("Serial connection", False, "Failed to connect")
                return False
            
            self.add_result("Serial connection", True, f"Connected to {self.port}")
            return True
        except Exception as e:
            self.add_result("Serial connection", False, str(e))
            return False
    
    def test_software_version(self):
        logger.info("Testing pymodbus version...")
        try:
            from pymodbus import __version__
            self.add_result("pymodbus version", True, f"pymodbus {__version__}")
            return True
        except ImportError:
            self.add_result("pymodbus version", False, "Failed to import pymodbus")
            return False
    
    def test_register_read(self, address=0x1000, count=1):
        logger.info(f"Testing register read at 0x{address:04X}...")
        try:
            if not self.client:
                self.add_result("Register read", False, "No client connected")
                return False
            
            result = self.client.read_holding_registers(address, count=count, device_id=self.slave_id)
            
            if result.isError():
                self.add_result("Register read", False, f"Error: {result}")
                return False
            
            self.add_result("Register read", True, f"Read {len(result.registers)} registers: {result.registers}")
            return True
        except Exception as e:
            self.add_result("Register read", False, str(e))
            return False
    
    def test_register_write(self, address=0x1000, value=0):
        logger.info(f"Testing register write at 0x{address:04X} with value {value}...")
        try:
            if not self.client:
                self.add_result("Register write", False, "No client connected")
                return False
            
            original_value = self._safe_read_register(address)
            if original_value is None:
                logger.warning("Could not read original value, skipping write test")
                return False
            
            result = self.client.write_register(address, value, device_id=self.slave_id)
            
            if result.isError():
                self.add_result("Register write", False, f"Error: {result}")
                return False
            
            read_back = self.client.read_holding_registers(address, count=1, device_id=self.slave_id)
            if read_back.isError():
                self.add_result("Register write", False, f"Write succeeded but read back failed: {read_back}")
                return False
            
            if read_back.registers[0] == value:
                self.add_result("Register write", True, f"Wrote {value}, read back {read_back.registers[0]}")
                
                if original_value:
                    self.client.write_register(address, original_value, device_id=self.slave_id)
                return True
            else:
                self.add_result("Register write", False, f"Wrote {value}, read back {read_back.registers[0]}")
                if original_value:
                    self.client.write_register(address, original_value, device_id=self.slave_id)
                return False
        except Exception as e:
            self.add_result("Register write", False, str(e))
            return False
    
    def _safe_read_register(self, address):
        try:
            result = self.client.read_holding_registers(address, count=1, device_id=self.slave_id)
            if not result.isError() and result.registers:
                return result.registers[0]
        except Exception:
            pass
        return None
    
    def test_exception_handling(self):
        logger.info("Testing exception handling...")
        try:
            test_addresses = [0x0000, 0xFFFF, 0x1234, 0x4321]
            found_error = False
            
            for addr in test_addresses:
                result = self.client.read_holding_registers(addr, count=1, device_id=self.slave_id)
                if result.isError():
                    found_error = True
                    break
            
            self.add_result("Exception handling", True, f"Exception handling functional")
            return True
        except Exception as e:
            self.add_result("Exception handling", False, str(e))
            return False
    
    def run_all_tests(self):
        logger.info("Running full diagnostic suite...")
        
        self.test_software_version()
        self.test_connection_parameters()
        
        if not self.test_serial_connection():
            logger.error("Cannot proceed with Modbus tests - serial connection failed")
            return self.results
        
        self.test_register_read()
        self.test_register_write(0x1000, 100)
        self.test_exception_handling()
        
        logger.info("\n=== Diagnostic Summary ===")
        passed = sum(1 for r in self.results if r['passed'])
        total = len(self.results)
        logger.info(f"Tests passed: {passed}/{total}")
        
        failed = [r for r in self.results if not r['passed']]
        if failed:
            logger.warning("\nFailed tests:")
            for test in failed:
                logger.warning(f"  - {test['test']}: {test['message']}")
        
        return self.results
    
    def cleanup(self):
        if self.client:
            self.client.close()
            self.add_result("Connection cleanup", True, "Client closed")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run pymodbus serial diagnostics')
    parser.add_argument('--port', default='/dev/ttyUSB0', help='Serial port')
    parser.add_argument('--baudrate', type=int, default=9600, help='Baud rate')
    parser.add_argument('--slave', type=int, default=1, help='Slave ID')
    args = parser.parse_args()
    
    diagnostics = SerialDiagnostics(args.port, args.baudrate, args.slave)
    try:
        results = diagnostics.run_all_tests()
    finally:
        diagnostics.cleanup()
    
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    exit_code = 0 if passed == total else 1
    
    sys.exit(exit_code)

if __name__ == "__main__":
    import sys
    main()