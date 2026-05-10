#!/usr/bin/env python3
"""
Quick immediate test of keyboard input handling.
This demonstrates that keys are detected without Enter.
"""

import sys
import time

def test_immediate_input():
    print("="*60)
    print(" IMMEDIATE KEYBOARD INPUT TEST")
    print("="*60)
    print("Testing if key presses are detected immediately...")
    print("\nWhat to expect:")
    print("✓ Press should be detected instantly")
    print("✓ No Enter key required")
    print("✓ Character should not echo to screen")
    print("✓ Press 'q' to exit")

    print("\n⏳ Test starting in 2 seconds...")
    time.sleep(2)

    try:
        import tty
        import termios
        import select

        fileno = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fileno)
        tty.setcbreak(fileno)

        print("✅ Immediate input mode activated")
        print("Press keys to test (letters, numbers, arrows, etc.)")
        print("Press 'q' to exit\n")

        key_count = 0
        max_keys = 15

        while key_count < max_keys:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                key = sys.stdin.read(1)
                key_count += 1

                # Handle arrow keys
                if key == '\x1b':
                    # Wait for next characters in escape sequence
                    time.sleep(0.01)
                    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                        next_key = sys.stdin.read(1)
                        if next_key == '[':
                            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                                direction = sys.stdin.read(1)
                                directions = {'A': 'UP', 'B': 'DOWN', 'C': 'RIGHT', 'D': 'LEFT'}
                                print(f"Key {key_count}: ARROW {directions.get(direction, 'UNKNOWN')}")
                        else:
                            print(f"Key {key_count}: ESCAPE SEQUENCE")
                elif key == 'q':
                    print("Key {key_count}: QUIT (exiting)".format(key_count=key_count))
                    break
                elif key == ' ':
                    print("Key {key_count}: SPACE".format(key_count=key_count))
                elif key.isdigit():
                    print(f"Key {key_count}: NUMBER {key}")
                elif key.isalpha():
                    print(f"Key {key_count}: LETTER {key.upper()}")
                elif key == '\r':
                    print(f"Key {key_count}: ENTER")
                elif key == '\n':
                    print(f"Key {key_count}: LINE FEED")
                else:
                    print(f"Key {key_count}: {repr(key)}")

                print(f"Total keys detected: {key_count}/{max_keys}")
                print("Keep pressing keys or 'q' to quit...")

            time.sleep(0.01)

        print("\n" + "="*60)
        if key_count >= 5:
            print("✅ TEST PASSED!")
            print("✅ Immediate keyboard input working correctly")
            print("✅ Ready for VFD control")
        else:
            print("⚠️  Limited detection (terminal may not support raw mode)")
            print("⚠️  Will use fallback mode automatically")
        print("="*60)

        termios.tcsetattr(fileno, termios.TCSADRAIN, old_settings)

    except Exception as e:
        print(f"\n⚠️  Note: {e}")
        print("Your terminal may not support immediate input mode.")
        print("The VFD controller will automatically use fallback mode.")
        print("\nFallback mode works by typing commands:")
        print("  Type 'space' + Enter for Start/Stop")
        print("  Type 'left' + Enter for Left direction")
        print("  Type 'right' + Enter for Right direction")
        print("  Type 'quit' + Enter to exit")

if __name__ == "__main__":
    try:
        test_immediate_input()
    except KeyboardInterrupt:
        print("\n\n✅ Test interrupted by user")
    except Exception as e:
        print(f"\n⚠️  Error: {e}")