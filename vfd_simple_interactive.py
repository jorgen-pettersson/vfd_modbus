#!/usr/bin/env python3
"""
Simplified interactive VFD controller with better keyboard handling.
This version focuses on reliable input without complex terminal handling.
"""

import argparse
import logging
import time
import sys
import signal
from vfd_test_controller import VFDTestController

logging.basicConfig(level=logging.WARNING)  # Reduce logging noise
logger = logging.getLogger(__name__)

class SimpleVFDController:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, slave_id=1):
        self.controller = VFDTestController(port, baudrate, slave_id)
        self.direction = 'FORWARD'
        self.speed = 0
        self.target_speed = 0
        self.running = False
        self.min_speed = 5
        self.max_speed = 100
        self.speed_step = 5

    def connect(self):
        if not self.controller.connect():
            return False
        return True

    def disconnect(self):
        if self.running:
            self.controller.ramp_stop()
        self.controller.disconnect()

    def execute_command(self, command):
        """Execute VFD commands based on input."""
        result = None

        if command == ' ':
            if self.running:
                self.controller.ramp_stop()
                self.running = False
                self.speed = 0
                result = "STOPPED"
            else:
                if self.direction == 'FORWARD':
                    self.controller.start_forward(self.target_speed)
                else:
                    self.controller.start_reverse(self.target_speed)
                self.running = True
                self.speed = self.target_speed if self.target_speed > 0 else 25
                result = "STARTED"

        elif command.lower() == 'l' or command.lower() == 'left':
            self.direction = 'REVERSE'
            result = "DIRECTION: REVERSE"
            if self.running:
                self.controller.ramp_stop()
                time.sleep(0.5)
                self.controller.start_reverse(self.speed)

        elif command.lower() == 'r' and self.direction == 'REVERSE':
            # Reset fault
            self.controller.fault_reset()
            result = "FAULT RESET"
        elif command.lower() == 'r' or command.lower() == 'right':
            self.direction = 'FORWARD'
            result = "DIRECTION: FORWARD"
            if self.running:
                self.controller.ramp_stop()
                time.sleep(0.5)
                self.controller.start_forward(self.speed)

        elif command.lower() == 'u' or command.lower() == 'up':
            if self.target_speed < self.max_speed:
                self.target_speed = min(self.target_speed + self.speed_step, self.max_speed)
                if self.running:
                    if self.direction == 'FORWARD':
                        self.controller.start_forward(self.target_speed)
                    else:
                        self.controller.start_reverse(self.target_speed)
                    self.speed = self.target_speed
                result = f"SPEED: {self.speed}%"
            else:
                result = "MAX SPEED REACHED"

        elif command.lower() == 'd' or command.lower() == 'down':
            if self.target_speed > self.min_speed:
                self.target_speed = max(self.target_speed - self.speed_step, self.min_speed)
                if self.running:
                    if self.direction == 'FORWARD':
                        self.controller.start_forward(self.target_speed)
                    else:
                        self.controller.start_reverse(self.target_speed)
                    self.speed = self.target_speed
                result = f"SPEED: {self.speed}%"
            else:
                result = "MIN SPEED REACHED"

        elif command.isdigit():
            digit = int(command)
            speed = 100 if digit == 0 else digit * 10
            self.target_speed = speed
            if self.running:
                if self.direction == 'FORWARD':
                    self.controller.start_forward(self.target_speed)
                else:
                    self.controller.start_reverse(self.target_speed)
                self.speed = self.target_speed
            result = f"SPEED SET: {self.speed}%"

        elif command.lower() == 's':
            status = self.controller.get_status()
            fault_code = self.controller.get_fault_code()
            result = f"STATUS: {status}, FAULT: {fault_code}"

        elif command.lower() == 'e':
            self.controller.emergency_stop()
            self.running = False
            self.speed = 0
            result = "EMERGENCY STOP"

        elif command.lower() == 'q':
            return None

        elif command.lower() == '?':
            return "HELP"

        return result

    def display_status(self):
        """Display current VFD status."""
        print("\033[H\033[J", end="")  # Clear screen

        print("="*60)
        direction_arrow = "→" if self.direction == 'FORWARD' else "←"
        status_icon = "✓ RUN" if self.running else "✗ STOP"
        print(f"    VFD CONTROL - {self.direction} {direction_arrow}    ")
        print("="*60)

        print(f"\n📊 STATUS:")
        print(f"   Running:  {status_icon}")
        print(f"   Direction: {direction_arrow} {self.direction}")
        print(f"   Speed:     {self.speed}%")
        print(f"   Target:    {self.target_speed}%")

        print(f"\n⌨️  COMMANDS:")
        print(f"   [space]    Start/Stop")
        print(f"   [l/r]      Left/Right direction")
        print(f"   [u/d]      Up/Down speed")
        print(f"   [0-9]      Set speed (5=50%, 0=100%)")
        print(f"   [s]        Show status")
        print(f"   [e]        Emergency stop")
        print(f"   [?]        Help")
        print(f"   [q]        Quit")

        print("="*60)
        print("Enter command (single key + Enter): ", end="", flush=True)

    def run_interactive(self):
        """Run the interactive control loop."""
        try:
            fileno = sys.stdin.fileno()
            import tty
            import termios
            import select

            old_settings = termios.tcgetattr(fileno)
            tty.setcbreak(fileno)

            self.display_status()
            print("Training mode: Type single key + Enter for commands")

        except Exception as e:
            # Fallback to standard input for terminals that don't support raw mode
            logger.info(f"Using fallback input mode: {e}")
            self.run_fallback()
            return

        try:

            while True:
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    key = sys.stdin.read(1)
                    result = self.execute_command(key)

                    if result is None:
                        break

                    self.display_status()

                time.sleep(0.01)

        except Exception as e:
            print(f"\nNote: Using fallback input method...")
            # Fallback to standard input
            self.run_fallback()

        finally:
            try:
                if 'old_settings' in locals():
                    termios.tcsetattr(fileno, termios.TCSADRAIN, old_settings)
            except:
                pass

    def run_fallback(self):
        """Fallback method using standard input."""
        self.display_status()
        print(f"\n(Waiting for Enter after each command)")

        while True:
            try:
                command = input("> ").strip().lower()
                if not command:
                    continue

                # Handle simple commands
                if len(command) == 1:
                    result = self.execute_command(command)
                else:
                    # Handle multi-character commands
                    if command in ['space', 'enter']:
                        result = self.execute_command(' ')
                    elif command in ['up', 'u']:
                        result = self.execute_command('u')
                    elif command in ['down', 'd']:
                        result = self.execute_command('d')
                    elif command in ['left', 'l']:
                        result = self.execute_command('l')
                    elif command in ['right', 'r']:
                        result = self.execute_command('r')
                    elif command == 'quit' or command == 'exit':
                        result = None
                    elif command == 'stop':
                        result = self.execute_command(' ')
                    elif command == 'start':
                        result = self.execute_command(' ')
                    elif command == 'reset':
                        result = self.execute_command('r')
                    elif command == 'emergency':
                        result = self.execute_command('e')
                    else:
                        print(f"Unknown command: {command}")
                        print("Type '?' for help, 'q' to quit")
                        continue

                if result is None:
                    break

                print(f"Result: {result}")
                self.display_status()

            except KeyboardInterrupt:
                break

def main():
    parser = argparse.ArgumentParser(description='Simple VFD interactive control')
    parser.add_argument('--port', default='/dev/ttyUSB0', help='Serial port')
    parser.add_argument('--baudrate', type=int, default=9600, help='Baud rate')
    parser.add_argument('--slave', type=int, default=1, help='Slave ID')
    args = parser.parse_args()

    def signal_handler(signum, frame):
        print("\n👋 Exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    controller = SimpleVFDController(args.port, args.baudrate, args.slave)

    if not controller.connect():
        print("Failed to connect to VFD")
        #return 1

    try:
        print("\n" + "="*60)
        print("   VFD INTERACTIVE CONTROL")
        print("="*60)
        print(f"Connected to {args.port} at {args.baudrate} baud")
        print("\nStarting interactive control...")

        controller.run_interactive()

        print("\n👋 Thank you for using VFD control!")
        return 0

    finally:
        controller.disconnect()

if __name__ == "__main__":
    sys.exit(main())