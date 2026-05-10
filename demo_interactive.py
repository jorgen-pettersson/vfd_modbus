#!/usr/bin/env python3
print("""
============================================================
   VFD INTERACTIVE CONTROL - DEMONSTRATION
============================================================

🎮 KEYBOARD CONTROLS:
   [SPACE]     Start/Stop motor
   [LEFT]      Toggle to REVERSE direction  
   [RIGHT]     Toggle to FORWARD direction
   [UP]        Increase speed (+5%)
   [DOWN]      Decrease speed (-5%)
   [0-9]       Set speed (5=50%, 0=100%)
   [r]         Reset VFD fault
   [s]         Show detailed VFD status
   [e]         Emergency stop
   [q]         Quit application

📊 REAL-TIME STATUS DISPLAY:
   - Running state (YES/NO)
   - Direction (FORWARD/REVERSE)  
   - Target speed percentage
   - Actual speed percentage
   - VFD real-time status
   - Fault condition monitoring

⚙️  CONFIGURATION:
   Default speed range: 5% - 100%
   Speed increment: 5%
   Start direction: FORWARD
   Initial state: STOPPED

🚀 STARTING INTERACTIVE CONTROL:
   1. Connect VFD via RS485 to /dev/ttyUSB0
   2. Ensure VFD is powered on
   3. Run: python3 vfd_interactive.py
   4. Use keyboard to control motor

⚠️  SAFETY:
   - Always start with low speed
   - Monitor VFD status during operation
   - Use ramp stop (SPACE) for normal shutdown
   - Emergency stop [e] for immediate halt
   - Check VFD faults before starting

Press any key to start interactive demo...
""")

input()

# Simulate interactive display update
import time

def show_status(running, direction, speed, target_speed, fault=False):
    print("\033[H\033[J", end="")  # Clear screen
    print("="*60)
    print(f"       VFD INTERACTIVE CONTROL - {direction}")
    print("="*60)
    
    status_icon = "✓ RUNNING" if running else "✗ STOPPED"
    direction_icon = "→ FORWARD" if direction == "FORWARD" else "← REVERSE"
    fault_status = "⚠️  FAULT" if fault else "✓ OK"
    
    print(f"\n📊 STATUS:")
    print(f"   Running:  {status_icon}")
    print(f"   Direction: {direction_icon}")
    print(f"   Target Speed: {target_speed}%")
    print(f"   Actual Speed: {speed}%")
    
    print(f"\n🔧 VFD REAL-TIME:")
    print(f"   Status: {status_icon}")
    print(f"   Direction: {direction_icon}")
    print(f"   Fault: {fault_status}")
    
    print(f"\n⌨️  CONTROLS: (type command and press Enter)")
    print(f"   [space] Start/Stop   [left] Reverse   [right] Forward")
    print(f"   [up] Speed+          [down] Speed-    [0-9] Set speed")
    print(f"   [r] Reset fault      [s] Status       [e] Emergency stop")
    
    print("="*60)
    print(f"Command > ", end="", flush=True)

# Demo sequence
demo_commands = [
    ("", False, "FORWARD", 0, 0, False),
    ("space", True, "FORWARD", 25, 25, False),
    ("up", True, "FORWARD", 30, 30, False),
    ("up", True, "FORWARD", 35, 35, False),
    ("left", True, "REVERSE", 35, 35, False),
    ("down", True, "REVERSE", 30, 30, False),
    ("space", False, "REVERSE", 0, 0, False),
    ("right", False, "FORWARD", 0, 0, False),
    ("5", True, "FORWARD", 50, 50, False),
    ("space", False, "FORWARD", 0, 0, False),
]

print("\n🎬 DEMONSTRATION SEQUENCE:")
print("   (This shows what the interactive display looks like)")
print("   Press Enter to start demo sequence...")
input()

print("\nStarting demo in 3 seconds...")
for i in range(3, 0, -1):
    print(f"{i}...", end="", flush=True)
    time.sleep(1)
print(" GO!\n")

for command, running, direction, speed, target_speed, fault in demo_commands:
    show_status(running, direction, speed, target_speed, fault)
    
    if command:
        print(command, flush=True)
    
    # Show what command does
    command_descriptions = {
        "": "Waiting for command...",
        "space": "Motor started/stopped",
        "up": "Speed increased by 5%",
        "down": "Speed decreased by 5%", 
        "left": "Direction changed to REVERSE",
        "right": "Direction changed to FORWARD",
        "5": "Speed set to 50%",
    }
    
    if command in command_descriptions:
        print(f"📌 {command_descriptions[command]}")
        print(f"   Press Enter for next action...", end="", flush=True)
        time.sleep(0.5)
        input()

print("\n" + "="*60)
print("   ✓ DEMONSTRATION COMPLETE")
print("="*60)
print("\n" + "="*60)
print("   READY TO USE WITH REAL VFD")
print("="*60)
print("""
To start controlling your actual VFD:

1. Connect VFD RS485 to /dev/ttyUSB0
2. Ensure VFD is powered on  
3. Run: python3 vfd_interactive.py
4. Use the keyboard controls shown above

Remember:
 - Start with low speeds (10-20%)
 - Monitor VFD status during operation
 - Use ramp stop for normal shutdown
 - Check VFD parameters P0.02 and P0.03
""")