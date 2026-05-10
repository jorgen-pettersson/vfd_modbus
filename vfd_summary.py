#!/usr/bin/env python3
"""
============================================================
   VFD TESTING SUITE - SUMMARY
============================================================

This project provides comprehensive testing and control
for T9000/9400 series Variable Frequency Drives via
Modbus RTU communication.

AVAILABLE COMPONENTS:

1. VFD CONTROLLER CORE:
   ├─ vfd_test_controller.py     - Main VFD control class
   ├─ vfd_basic_commands.py      - Automated test suite
   └─ vfd_test_setup.py          - Setup verification

2. INTERACTIVE CONTROL (NEW!):
   ├─ vfd_interactive.py         - Keyboard-based control
   ├─ demo_vfd_interactive.py    - Interactive demo
   └─ test_vfd_interactive.py    - Interactive setup test

3. TESTING INFRASTRUCTURE:
   ├─ detect_serial.py           - Serial port detection
   ├─ serial_diagnostics.py      - Full diagnostic suite
   ├─ test_serial.py             - Automated test runner
   └─ vfd_control.py             - Original VFD control script

QUICK START:

1. SETUP VERIFICATION:
   python3 vfd_test_setup.py
   python3 test_vfd_interactive.py

2. HARDWARE TESTING:
   python3 detect_serial.py
   python3 vfd_test_controller.py --status

3. AUTOMATED TESTS:
   python3 vfd_basic_commands.py --test all

4. INTERACTIVE CONTROL:
   python3 vfd_interactive.py
   python3 demo_vfd_interactive.py

INTERACTIVE KEYBOARD CONTROLS:

   [SPACE]     Start/Stop motor
   [LEFT]      Reverse direction
   [RIGHT]     Forward direction  
   [UP]        Increase speed (+5%)
   [DOWN]      Decrease speed (-5%)
   [0-9]       Set speed (5=50%, 0=100%)
   [r]         Reset fault
   [s]         Show detailed status
   [e]         Emergency stop
   [q]         Quit

VFD SPECIFICATION (T9000/9400):

REGISTERS:
   0x1000  - Speed control (0-10000 = 0-100%)
   0x2000  - Command register (1=Forward, 2=Reverse, 6=Stop, 7=Reset)
   0x3000  - Status register (bit0=running, bit1=reverse, bit2=fault)
   0x8000  - Fault code
   0x8001  - Communication fault

COMMANDS:
   0x2000 = 1  - Run Forward
   0x2000 = 2  - Run Reverse
   0x2000 = 5  - Coast Stop
   0x2000 = 6  - Deceleration Stop (preferred)
   0x2000 = 7  - Fault Reset

REQUIREMENTS:

VFD PARAMETERS:
   P0.02 = 2  # Command source = communication
   P0.03 = 9  # Frequency source = communication

RS485 WIRING:
   VFD RS+ → RS485 A / D+
   VFD RS- → RS485 B / D-
   VFD GND → Adapter GND

COMMUNICATION:
   Protocol: Modbus RTU
   Baudrate: 9600, 8N1
   Slave ID: 1

SAFETY PRECAUTIONS:

   - Always test with low speeds first (10-20%)
   - Verify VFD parameters before operation
   - Monitor VFD status during operation
   - Use ramp stop for normal shutdown
   - Emergency stop available via [e] key
   - Check for faults before starting motor

CONFIGURATION OPTIONS:

VFD Controller:
   --port /dev/ttyUSB0          # Serial port
   --baudrate 9600              # Communication speed
   --slave 1                    # Modbus slave ID

Interactive Control:
   --min-speed 5                # Minimum speed %
   --max-speed 100              # Maximum speed %
   --speed-step 5               # Speed increment %

DOCUMENTATION:

   README.md                    - Complete documentation
   doc/T9000.pdf                - VFD specification

GETTING HELP:

   python3 vfd_test_controller.py --help
   python3 vfd_basic_commands.py --help
   python3 vfd_interactive.py --help

TESTING WORKFLOW:

1. Setup:
   python3 vfd_test_setup.py
   python3 test_vfd_interactive.py

2. Connection:
   python3 detect_serial.py
   python3 vfd_test_controller.py --status

3. Basic Tests:
   python3 vfd_basic_commands.py --test start_stop
   python3 vfd_basic_commands.py --test direction

4. Advanced Tests:
   python3 vfd_basic_commands.py --test all

5. Interactive Control:
   python3 vfd_interactive.py

FILES OVERVIEW:

Core Files:
   vfd_test_controller.py     - Main VFD control class (250 lines)
   vfd_basic_commands.py      - Test suite with 6 scenarios (350 lines)
   vfd_interactive.py         - Interactive keyboard control (320 lines)

Testing Files:
   vfd_test_setup.py          - Setup verification (100 lines)
   test_vfd_interactive.py    - Interactive setup test (120 lines)
   demo_vfd_interactive.py   - Interactive demonstration (120 lines)

Infrastructure:
   detect_serial.py           - Serial port detection (120 lines)
   serial_diagnostics.py      - Full diagnostics (250 lines)
   test_serial.py             - Test automation (200 lines)

Total Lines: ~1,800 lines of code
Test Coverage: 6 comprehensive test scenarios
Interactive Features: Real-time keyboard control

============================================================
"""

def main():
    print(__doc__)
    
    print("\n" + "="*60)
    print("   READY TO START VFD TESTING")
    print("="*60)
    
    print("\nChoose your starting point:")
    print("1. Setup Verification")
    print("2. Hardware Connection Test")  
    print("3. Automated Test Suite")
    print("4. Interactive Keyboard Control")
    print("5. Run Demo")
    
    choice = input("\nSelect option (1-5) or press Enter for status check: ")
    
    if choice == "1":
        print("\nRunning setup verification...")
        import subprocess
        subprocess.run(["python3", "vfd_test_setup.py"])
        
    elif choice == "2":
        print("\nRunning connection test...")
        import subprocess
        subprocess.run(["python3", "detect_serial.py"])
        
    elif choice == "3":
        print("\nRunning automated test suite...")
        print("This will test all basic VFD commands")
        test = input("Run all tests? (y/n): ")
        if test.lower() == 'y':
            import subprocess
            subprocess.run(["python3", "vfd_basic_commands.py", "--test", "all"])
        
    elif choice == "4":
        print("\nStarting interactive VFD control...")
        print("Ensure VFD is connected and powered on")
        ready = input("Ready to start? (y/n): ")
        if ready.lower() == 'y':
            import subprocess
            subprocess.run(["python3", "vfd_interactive.py"])
        
    elif choice == "5":
        print("\nRunning interactive demo...")
        import subprocess
        subprocess.run(["python3", "demo_vfd_interactive.py"])
        
    else:
        print("\nRunning quick status check...")
        import subprocess
        subprocess.run(["python3", "vfd_test_controller.py", "--status"])

if __name__ == "__main__":
    main()