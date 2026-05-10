#!/usr/bin/env python3
import glob
import os
import sys
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERIAL_PATTERNS = [
    "/dev/ttyUSB*",      # USB serial ports
    "/dev/ttyACM*",      # USB CDC devices
    "/dev/ttyAMA*",      # Raspberry Pi hardware serial
    "/dev/ttyS*",        # Standard serial ports
]

def detect_serial_ports():
    ports = []
    seen = set()
    
    for pattern in SERIAL_PATTERNS:
        for port_path in glob.glob(pattern):
            if port_path not in seen:
                seen.add(port_path)
                ports.append(port_path)
    
    logger.info(f"Found {len(ports)} serial port(s): {ports}")
    return sorted(ports)

def check_port_accessibility(port):
    port_path = Path(port)
    
    if not port_path.exists():
        logger.error(f"Port {port} does not exist")
        return False
    
    if not os.access(port, os.R_OK | os.W_OK):
        logger.error(f"Port {port} exists but no read/write permission")
        current_user = os.getlogin()
        logger.info(f"  Current user: {current_user}")
        logger.info(f"  Port permissions: {oct(os.stat(port).st_mode)[-3:]}")
        logger.info(f"  Try: sudo usermod -a -G dialout {current_user}")
        return False
    
    logger.info(f"Port {port} is accessible")
    return True

def test_basic_serial(port, baudrate=9600):
    try:
        import serial
        logger.info(f"Testing basic serial communication on {port} at {baudrate} baud...")
        ser = serial.Serial(port, baudrate, timeout=1)
        ser.close()
        logger.info("Basic serial test passed")
        return True
    except ImportError:
        logger.warning("pyserial not installed, skipping serial test")
        logger.info("Install with: pip install pyserial")
        return None
    except serial.SerialException as e:
        logger.error(f"Serial test failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

def get_port_info(port):
    try:
        if os.path.exists(port):
            stat = os.stat(port)
            return {
                'path': port,
                'exists': True,
                'size': stat.st_size,
                'mode': oct(stat.st_mode)[-3:],
                'uid': stat.st_uid,
                'gid': stat.st_gid,
            }
    except Exception as e:
        return {'path': port, 'exists': False, 'error': str(e)}
    return {'path': port, 'exists': False}

def main():
    parser = argparse.ArgumentParser(description='Detect and test serial ports')
    parser.add_argument('--port', help='Test specific port')
    parser.add_argument('--baudrate', type=int, default=9600, help='Baud rate for test')
    parser.add_argument('--test', action='store_true', help='Test serial communication')
    args = parser.parse_args()
    
    if args.port:
        logger.info(f"Checking specific port: {args.port}")
        if check_port_accessibility(args.port):
            if args.test:
                result = test_basic_serial(args.port, args.baudrate)
                if result is False:
                    sys.exit(1)
            sys.exit(0)
        sys.exit(1)
    
    ports = detect_serial_ports()
    
    if not ports:
        logger.error("No serial ports found. Connect your USB serial adapter first.")
        logger.info("Common USB adapters:")
        logger.info("  - FTDI chips: /dev/ttyUSB0")
        logger.info("  - CP2102/CP2104: /dev/ttyUSB0 or /dev/ttyACM0")
        logger.info("  - CH340: /dev/ttyUSB0")
        sys.exit(1)
    
    logger.info("\nPort details:")
    for port in ports:
        info = get_port_info(port)
        logger.info(f"  {port}: accessible={check_port_accessibility(port)}")
    
    logger.info(f"\nRecommended port for pymodbus: {ports[0]}")
    logger.info(f"Usage: python pymodbus.py --port {ports[0]}")
    
    if args.test:
        logger.info("\nTesting serial communication on all available ports...")
        for port in ports:
            test_basic_serial(port, args.baudrate)

if __name__ == "__main__":
    main()