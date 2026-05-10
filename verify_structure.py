#!/usr/bin/env python3
"""
Quick test to verify the reorganized project structure.
"""

import os

def check_structure():
    print("="*60)
    print(" PROJECT STRUCTURE VERIFICATION")
    print("="*60)

    expected_dirs = [
        'tests',
        'tests/unit',
        'tests/integration', 
        'tests/demos',
        'tests/utils'
    ]

    required_files = [
        'vfd_test_controller.py',
        'vfd_simple_interactive.py',
        'detect_serial.py',
        'serial_diagnostics.py',
        'demo_interactive.py',
        'README.md',
        'run_tests.py'
    ]

    required_tests = [
        'tests/unit/test_controller_setup.py',
        'tests/unit/test_interactive.py',
        'tests/unit/test_input.py',
        'tests/unit/test_simple.py',
        'tests/integration/test_serial_comm.py',
        'tests/integration/test_basic_commands.py',
        'tests/utils/final_system_test.py'
    ]

    print("\n✓ Checking directory structure...")
    missing_dirs = []
    for dir_path in expected_dirs:
        if os.path.isdir(dir_path):
            print(f"   ✓ {dir_path}/")
        else:
            print(f"   ✗ {dir_path}/ (MISSING)")
            missing_dirs.append(dir_path)

    print("\n✓ Checking main files...")
    missing_main = []
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"   ✓ {file_path}")
        else:
            print(f"   ✗ {file_path} (MISSING)")
            missing_main.append(file_path)

    print("\n✓ Checking test files...")
    missing_tests = []
    for test_file in required_tests:
        if os.path.isfile(test_file):
            print(f"   ✓ {test_file}")
        else:
            print(f"   ✗ {test_file} (MISSING)")
            missing_tests.append(test_file)

    # Check removed files
    print("\n✓ Checking deprecated files removed...")
    deprecated_files = [
        'vfd_interactive.py',
        'vfd_control.py',
        'vfd_input_resolved.py',
        'vfd_interactive_fixed.py'
    ]

    removed_count = 0
    for file_path in deprecated_files:
        if not os.path.isfile(file_path):
            print(f"   ✓ {file_path} (removed)")
            removed_count += 1
        else:
            print(f"   ✗ {file_path} (still present - should be removed)")

    # Summary
    print("\n" + "="*60)
    print(" VERIFICATION SUMMARY")
    print("="*60)

    all_good = True

    if missing_dirs:
        print(f"✗ {len(missing_dirs)} missing directories")
        all_good = False
    else:
        print("✓ All expected directories present")

    if missing_main:
        print(f"✗ {len(missing_main)} missing main files")
        all_good = False
    else:
        print("✓ All required main files present")

    if missing_tests:
        print(f"✗ {len(missing_tests)} missing test files")
        all_good = False
    else:
        print("✓ All required test files present")

    if removed_count == len(deprecated_files):
        print("✓ All deprecated files removed")
    else:
        print(f"⚠ {removed_count}/{len(deprecated_files)} deprecated files removed")

    if all_good:
        print("\n✅ REORGANIZATION COMPLETE!")
        print("\nNew structure:")
        print("   Main directory: Core applications")
        print("   tests/unit/: Component testing")
        print("   tests/integration/: System testing")
        print("   tests/utils/: Utilities and diagnostics")
        print("   tests/demos/: Example usage (empty)")
        return 0
    else:
        print("\n❌ Some issues found during verification")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(check_structure())