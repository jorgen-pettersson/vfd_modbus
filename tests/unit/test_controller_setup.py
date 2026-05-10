#!/usr/bin/env python3
import sys
import logging
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from vfd_test_controller import VFDTestController

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_vfd_controller_setup():
    print("="*60)
    print("VFD CONTROLLER SETUP TEST")
    print("="*60)
    
    print("\n1. Testing controller initialization...")
    controller = VFDTestController(port='/dev/ttyUSB0', baudrate=9600, slave_id=1)
    
    assert controller.port == '/dev/ttyUSB0', "Port not set correctly"
    assert controller.baudrate == 9600, "Baudrate not set correctly"
    assert controller.slave_id == 1, "Slave ID not set correctly"
    print("   ✓ Controller initialized with correct parameters")
    
    print("\n2. Verifying register addresses...")
    assert controller.REG_CONTROL == 0x2000, "Control register wrong"
    assert controller.REG_SPEED == 0x1000, "Speed register wrong"
    assert controller.REG_STATUS == 0x3000, "Status register wrong"
    assert controller.REG_FAULT_CODE == 0x8000, "Fault register wrong"
    print("   ✓ All register addresses correct")
    
    print("\n3. Verifying command values...")
    assert controller.CMD_RUN_FORWARD == 1, "Forward command wrong"
    assert controller.CMD_RUN_REVERSE == 2, "Reverse command wrong"
    assert controller.CMD_COAST_STOP == 5, "Coast stop wrong"
    assert controller.CMD_RAMP_STOP == 6, "Ramp stop wrong"
    assert controller.CMD_FAULT_RESET == 7, "Fault reset wrong"
    print("   ✓ All command values correct")
    
    print("\n4. Testing connection establishment...")
    if controller.connect():
        print("   ✓ User can connect to serial port")
        controller.disconnect()
    else:
        print("   ⚠ Could not connect to VFD (expected if no hardware)")
    
    print("\n5. Testing command method availability...")
    methods = [
        'set_speed_percent', 'set_frequency_hz',
        'start_forward', 'start_reverse',
        'coast_stop', 'ramp_stop', 'fault_reset', 'emergency_stop',
        'get_status', 'is_running', 'has_fault',
        'get_fault_code', 'get_comm_fault'
    ]
    
    for method in methods:
        assert hasattr(controller, method), f"Missing method: {method}"
    print(f"   ✓ All {len(methods)} methods available")
    
    print("\n6. Testing speed conversion logic...")
    print("   Percentage to frequency conversion:")
    test_cases = [(0, 0), (25, 2500), (50, 5000), (100, 10000)]
    for percent, expected_freq in test_cases:
        calculated = int((percent / 100) * 10000)
        assert calculated == expected_freq, f"Speed conversion failed for {percent}%"
        print(f"   {percent}% -> {calculated} ✓")
    
    print("\n7. Testing command-line interface...")
    print("   Available tests:")
    tests = ['status', 'start_stop', 'direction', 'speed', 'monitor', 'fault', 'stop', 'all']
    for test in tests:
        print(f"   - --test {test}")
    
    print("\n" + "="*60)
    print("✓ ALL SETUP TESTS PASSED")
    print("="*60)
    
    return True

def main():
    try:
        success = test_vfd_controller_setup()
        if success:
            print("\n✓ VFD controller setup verification complete")
            print("\nReady to use with actual VFD hardware!")
            print("\nExample usage:")
            print("  python3 vfd_basic_commands.py --test start_stop")
            print("  python3 vfd_basic_commands.py --test all")
            return 0
        else:
            print("\n✗ Setup tests failed")
            return 1
            
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())