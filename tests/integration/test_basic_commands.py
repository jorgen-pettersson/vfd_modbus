#!/usr/bin/env python3
import argparse
import time
import logging
from vfd_test_controller import VFDTestController

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_basic_start_stop(controller):
    print("\n" + "="*60)
    print("TEST 1: Basic Start/Stop (Forward)")
    print("="*60)
    
    speed = 25
    
    print(f"\n1. Starting VFD forward at {speed}% speed...")
    if not controller.start_forward(speed):
        return False
    time.sleep(2)
    
    status = controller.get_status()
    if not status or not status['running']:
        print("FAILED: VFD should be running")
        return False
    print(f"SUCCESS: VFD is running forward at {speed}%")
    
    print("\n2. Stopping VFD with ramp stop...")
    controller.ramp_stop()
    time.sleep(1)
    
    status = controller.get_status()
    if status and status['running']:
        print("WARNING: VFD still running (normal during ramp)")
    else:
        print("SUCCESS: VFD stopped")
    
    return True

def test_direction_change(controller):
    print("\n" + "="*60)
    print("TEST 2: Direction Change (Forward -> Reverse)")
    print("="*60)
    
    speed = 20
    
    print(f"\n1. Starting VFD forward at {speed}% speed...")
    if not controller.start_forward(speed):
        return False
    time.sleep(2)
    
    status = controller.get_status()
    if not status or not status['running']:
        print("FAILED: VFD should be running forward")
        return False
    print(f"SUCCESS: VFD running forward (reverse={status['reverse']})")
    
    print("\n2. Stopping VFD...")
    controller.ramp_stop()
    time.sleep(1)
    
    print("\n3. Starting VFD reverse at {speed}% speed...".format(speed=speed))
    if not controller.start_reverse(speed):
        return False
    time.sleep(2)
    
    status = controller.get_status()
    if not status or not status['running']:
        print("FAILED: VFD should be running reverse")
        return False
    
    if not status['reverse']:
        print("FAILED: VFD should be running in reverse")
        return False
    print(f"SUCCESS: VFD running reverse (reverse={status['reverse']})")
    
    print("\n4. Coast stopping VFD...")
    controller.coast_stop()
    time.sleep(1)
    
    print("SUCCESS: Direction change test completed")
    return True

def test_speed_control(controller):
    print("\n" + "="*60)
    print("TEST 3: Speed Control")
    print("="*60)
    
    print("\n1. Setting speed via percentage...")
    speeds = [10, 25, 50, 75, 100]
    
    for speed in speeds:
        print(f"   Setting speed to {speed}%...")
        controller.set_speed_percent(speed)
        time.sleep(0.5)
        print(f"   Speed set to {speed}%")
    
    print("\n2. Setting speed via frequency...")
    frequencies = [10, 25, 40]
    
    for hz in frequencies:
        print(f"   Setting frequency to {hz}Hz...")
        controller.set_frequency_hz(hz)
        time.sleep(0.5)
        print(f"   Frequency set to {hz}Hz")
    
    print("SUCCESS: Speed control tests completed")
    return True

def test_status_monitoring(controller):
    print("\n" + "="*60)
    print("TEST 4: Status Monitoring")
    print("="*60)
    
    print("\n1. Reading initial status...")
    status = controller.get_status()
    if not status:
        print("FAILED: Could not read status")
        return False
    print(f"   Initial status: Running={status['running']}, Reverse={status['reverse']}, Fault={status['fault']}")
    
    print("\n2. Testing is_running()...")
    if controller.has_fault():
        print("   VFD has fault, attempting reset...")
        controller.fault_reset()
        time.sleep(1)
    
    running = controller.is_running()
    print(f"   VFD running: {running}")
    
    print("\n3. Starting VFD and monitoring status...")
    controller.start_forward(30)
    time.sleep(2)
    
    for i in range(3):
        status = controller.get_status()
        print(f"   Status check {i+1}: Running={status['running']}, "
              f"Reverse={status['reverse']}, Fault={status['fault']}")
        time.sleep(1)
    
    print("\n4. Stopping and checking fault codes...")
    controller.ramp_stop()
    time.sleep(1)
    
    fault_code = controller.get_fault_code()
    comm_fault = controller.get_comm_fault()
    
    print(f"   Fault code: {fault_code}")
    print(f"   Comm fault: {comm_fault}")
    
    if fault_code == 0 and comm_fault == 0:
        print("SUCCESS: No faults detected")
    else:
        print("WARNING: Faults detected (may be expected)")
    
    return True

def test_fault_handling(controller):
    print("\n" + "="*60)
    print("TEST 5: Fault Handling")
    print("="*60)
    
    print("\n1. Checking for existing faults...")
    has_fault = controller.has_fault()
    fault_code = controller.get_fault_code()
    
    print(f"   Has fault: {has_fault}")
    print(f"   Fault code: {fault_code}")
    
    if fault_code and fault_code > 0:
        print("\n2. Attempting fault reset...")
        if controller.fault_reset():
            print("   Fault reset command sent")
            time.sleep(1)
            
            fault_code_after = controller.get_fault_code()
            if fault_code_after == 0:
                print("   SUCCESS: Fault cleared")
            else:
                print(f"   WARNING: Fault still active (code: {fault_code_after})")
        else:
            print("   FAILED: Could not send fault reset command")
    else:
        print("   No faults to reset")
    
    print("\n3. Testing fault status detection...")
    status = controller.get_status()
    print(f"   Fault status: {status['fault']}")
    
    print("SUCCESS: Fault handling test completed")
    return True

def test_stop_methods(controller):
    print("\n" + "="*60)
    print("TEST 6: Stop Methods Comparison")
    print("="*60)
    
    speed = 50
    
    print("\n1. Testing Ramp Stop (deceleration)...")
    controller.start_forward(speed)
    time.sleep(2)
    print("   VFD running at {speed}% speed".format(speed=speed))
    
    print("   Initiating ramp stop...")
    start_time = time.time()
    controller.ramp_stop()
    
    time.sleep(2)
    run_time = time.time() - start_time
    print(f"   Ramp stop initiated (running for {run_time:.1f}s total)")
    
    print("\n2. Testing Coast Stop (immediate)...")
    controller.start_forward(speed)
    time.sleep(2)
    print("   VFD running at {speed}% speed".format(speed=speed))
    
    print("   Initiating coast stop...")
    start_time = time.time()
    controller.coast_stop()
    
    time.sleep(1)
    run_time = time.time() - start_time
    print(f"   Coast stop initiated (running for {run_time:.1f}s total)")
    
    print("SUCCESS: Stop methods comparison completed")
    return True

def run_all_tests(controller):
    print("\n" + "="*60)
    print("RUNNING ALL VFD TESTS")
    print("="*60)
    
    tests = [
        ("Basic Start/Stop", test_basic_start_stop),
        ("Direction Change", test_direction_change),
        ("Speed Control", test_speed_control),
        ("Status Monitoring", test_status_monitoring),
        ("Fault Handling", test_fault_handling),
        ("Stop Methods", test_stop_methods),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*60}")
            print(f"RUNNING: {test_name}")
            print(f"{'='*60}")
            
            result = test_func(controller)
            results.append((test_name, result))
            
            if result:
                print(f"\n✓ {test_name}: PASSED")
            else:
                print(f"\n✗ {test_name}: FAILED")
            
            print(f"\nPausing 2 seconds between tests...")
            time.sleep(2)
            
        except Exception as e:
            print(f"\n✗ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60)
    
    return passed == total

def main():
    parser = argparse.ArgumentParser(description='Test basic VFD commands')
    parser.add_argument('--port', default='/dev/ttyUSB0', help='Serial port')
    parser.add_argument('--baudrate', type=int, default=9600, help='Baud rate')
    parser.add_argument('--slave', type=int, default=1, help='Modbus slave ID')
    parser.add_argument('--test', choices=['status', 'start_stop', 'direction', 'speed', 'monitor', 'fault', 'stop', 'all'],
                       help='Run specific test (default: all)', default='all')
    args = parser.parse_args()
    
    controller = VFDTestController(args.port, args.baudrate, args.slave)
    
    try:
        if not controller.connect():
            print("Failed to connect to VFD")
            return 1
        
        print("VFD Connected Successfully!")
        print(f"Port: {args.port}, Baudrate: {args.baudrate}, Slave ID: {args.slave}")
        
        if args.test == 'status':
            test_status_monitoring(controller)
        elif args.test == 'start_stop':
            test_basic_start_stop(controller)
        elif args.test == 'direction':
            test_direction_change(controller)
        elif args.test == 'speed':
            test_speed_control(controller)
        elif args.test == 'monitor':
            test_status_monitoring(controller)
        elif args.test == 'fault':
            test_fault_handling(controller)
        elif args.test == 'stop':
            test_stop_methods(controller)
        elif args.test == 'all':
            success = run_all_tests(controller)
            return 0 if success else 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        print("Ensuring VFD is stopped...")
        controller.emergency_stop()
        return 0
    except Exception as e:
        print(f"\nError: {e}")
        return 1
    finally:
        controller.disconnect()

if __name__ == "__main__":
    import sys
    sys.exit(main())