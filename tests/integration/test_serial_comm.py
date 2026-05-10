#!/usr/bin/env python3
import subprocess
import sys
import argparse
import logging
from pathlib import Path
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SerialTestRunner:
    def __init__(self, port=None, baudrate=9600, slave=1, auto_detect=True):
        self.port = port
        self.baudrate = baudrate
        self.slave = slave
        self.auto_detect = auto_detect
    
    def run_command(self, command, description):
        logger.info(f"Running: {description}")
        logger.info(f"Command: {command}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.stdout:
                print(result.stdout)
            
            if result.stderr:
                logger.error(f"Error output: {result.stderr}")
            
            if result.returncode != 0:
                logger.error(f"Command failed with code {result.returncode}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Failed to run command: {e}")
            return False
    
    def detect_serial_ports(self):
        if not self.auto_detect:
            return self.port
        
        logger.info("Auto-detecting serial ports...")
        if self.run_command("python3 detect_serial.py", "Serial port detection"):
            self.port = '/dev/ttyUSB0'  # Default for most USB adapters
            logger.info(f"Using detected port: {self.port}")
            return self.port
        return None
    
    def run_dry_run_test(self):
        if not self.port:
            logger.error("No port specified, cannot run dry-run test")
            return False
        
        logger.info("Running dry-run test (no actual Modbus operations)...")
        cmd = f"python3 vfd_control.py --port {self.port} --dry-run"
        return self.run_command(cmd, "Dry-run test")
    
    def run_diagnostics(self):
        if not self.port:
            logger.error("No port specified, cannot run diagnostics")
            return False
        
        logger.info("Running full diagnostic suite...")
        cmd = f"python3 serial_diagnostics.py --port {self.port} --baudrate {self.baudrate} --slave {self.slave}"
        return self.run_command(cmd, "Full diagnostics")
    
    def run_actual_test(self):
        if not self.port:
            logger.error("No port specified, cannot run actual test")
            return False
        
        logger.info("Running actual Modbus test (with VFD operations)...")
        logger.warning("This will attempt to control the VFD!")
        
        response = input("Continue with actual Modbus operations? (y/N): ")
        if response.lower() != 'y':
            logger.info("Test cancelled by user")
            return False
        
        cmd = f"python3 vfd_control.py --port {self.port} --baudrate {self.baudrate} --slave {self.slave}"
        return self.run_command(cmd, "Actual Modbus test")
    
    def run_basic_serial_test(self):
        if not self.port:
            logger.error("No port specified, cannot run basic serial test")
            return False
        
        logger.info("Running basic serial communication test...")
        cmd = f"python3 detect_serial.py --port {self.port} --test"
        return self.run_command(cmd, "Basic serial test")
    
    def main(self):
        logger.info("=== pymodbus Serial Test Suite ===")
        logger.info(f"Configuration: port={self.port}, baudrate={self.baudrate}, slave={self.slave}")
        
        if not self.port:
            logger.info("Step 1: Detecting serial ports...")
            self.port = self.detect_serial_ports()
            if not self.port:
                logger.error("Failed to detect serial ports. Please connect a USB serial adapter.")
                return False
        
        logger.info(f"Using serial port: {self.port}")
        
        print("\n" + "="*50)
        print("Available tests:")
        print("1. Basic serial communication test")
        print("2. Dry-run test (no Modbus operations)")
        print("3. Full diagnostics")
        print("4. Actual Modbus test (VFD control)")
        print("5. Run all tests")
        print("="*50)
        
        try:
            choice = input("\nSelect test (1-5): ").strip()
            if not choice:
                choice = "5"
        except (EOFError, KeyboardInterrupt):
            logger.info("\nTest cancelled by user")
            return False
        
        results = []
        
        if choice == "1":
            results.append(self.run_basic_serial_test())
        elif choice == "2":
            results.append(self.run_dry_run_test())
        elif choice == "3":
            results.append(self.run_diagnostics())
        elif choice == "4":
            results.append(self.run_actual_test())
        elif choice == "5":
            logger.info("Running all tests sequentially...")
            results.append(self.run_basic_serial_test())
            if results[-1]:
                results.append(self.run_dry_run_test())
            if results[-1]:
                results.append(self.run_diagnostics())
            
            if all(results):
                logger.info("All tests passed! You may proceed with actual Modbus operations.")
                response = input("Run actual Modbus test? (y/N): ")
                if response.lower() == 'y':
                    results.append(self.run_actual_test())
        else:
            logger.error(f"Invalid choice: {choice}")
            return False
        
        success_rate = sum(1 for r in results if r) / len(results) if results else 0
        logger.info(f"\nTest summary: {sum(1 for r in results if r)}/{len(results)} passed ({success_rate:.0%})")
        
        return all(results)

def main():
    parser = argparse.ArgumentParser(description='Automated pymodbus serial testing')
    parser.add_argument('--port', help='Serial port (auto-detect if not specified)')
    parser.add_argument('--baudrate', type=int, default=9600, help='Baud rate')
    parser.add_argument('--slave', type=int, default=1, help='Slave ID')
    parser.add_argument('--no-detect', action='store_true', help='Disable auto-detection')
    parser.add_argument('--basic', action='store_true', help='Run basic serial test only')
    parser.add_argument('--dry-run', action='store_true', help='Run dry-run test only')
    parser.add_argument('--diagnostic', action='store_true', help='Run diagnostics only')
    parser.add_argument('--actual', action='store_true', help='Run actual Modbus test only')
    args = parser.parse_args()
    
    runner = SerialTestRunner(
        port=args.port,
        baudrate=args.baudrate,
        slave=args.slave,
        auto_detect=not args.no_detect
    )
    
    if args.basic:
        if not runner.port:
            runner.port = runner.detect_serial_ports()
        sys.exit(0 if runner.run_basic_serial_test() else 1)
    elif args.dry_run:
        if not runner.port:
            runner.port = runner.detect_serial_ports()
        sys.exit(0 if runner.run_dry_run_test() else 1)
    elif args.diagnostic:
        if not runner.port:
            runner.port = runner.detect_serial_ports()
        sys.exit(0 if runner.run_diagnostics() else 1)
    elif args.actual:
        if not runner.port:
            runner.port = runner.detect_serial_ports()
        sys.exit(0 if runner.run_actual_test() else 1)
    else:
        success = runner.main()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()