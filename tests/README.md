# VFD Testing Suite

Organized testing suite for VFD control system.

## Test Categories

### Unit Tests (`tests/unit/`)
Individual component and functionality tests:
- `test_controller_setup.py` - VFD controller initialization and configuration
- `test_interactive.py` - Interactive controller setup and methods
- `test_input.py` - Keyboard input handling verification
- `test_simple.py` - Simple controller functionality tests

### Integration Tests (`tests/integration/`)
End-to-end testing of complete VFD operations:
- `test_serial_comm.py` - Serial communication and connectivity
- `test_basic_commands.py` - Complete VFD command sequences

### Utilities (`tests/utils/`)
Helper utilities and comprehensive tests:
- `final_system_test.py` - Full system verification

## Running Tests

### Run All Tests
```bash
python3 run_tests.py
```

### Run Specific Category
```bash
# Unit tests only
python3 run_tests.py --category unit

# Integration tests only
python3 run_tests.py --category integration
```

### Run Individual Test
```bash
# Run specific test file
python3 run_tests.py --test unit/test_controller_setup.py

# Or run directly
python3 tests/unit/test_controller_setup.py
```

## Test Requirements

Most tests can run without actual VFD hardware for development:

**No Hardware Required:**
- `test_controller_setup.py`
- `test_interactive.py` 
- `test_input.py`
- `test_simple.py`
- `final_system_test.py`

**Hardware Required:**
- `test_serial_comm.py` - Requires serial port connection
- `test_basic_commands.py` - Requires actual VFD device

## Development Testing

For development without hardware:
```bash
# Run hardware-independent tests
python3 run_tests.py --category unit
```

For production testing with hardware:
```bash
# Run full test suite with VFD connected
python3 run_tests.py
```

## Test Files Description

### test_controller_setup.py
Verifies VFD controller initialization:
- Configuration parameters
- Register addresses
- Command values
- Speed conversion logic
- Method availability

### test_interactive.py
Tests interactive controller functionality:
- Controller initialization
- Default configuration
- Speed setting methods
- Direction control
- Command execution
- Status display

### test_input.py
Validates keyboard input handling:
- Immediate key detection
- Arrow key recognition
- Character processing
- Terminal compatibility
- Fallback mode testing

### test_simple.py
Simple controller verification:
- Basic functionality
- Command parsing
- Speed and direction control
- Status updates

### test_serial_comm.py
Serial communication testing:
- Port detection and accessibility
- Connection establishment
- Basic serial operations
- Communication verification

### test_basic_commands.py
Complete VFD command sequences:
- Start/stop operations
- Direction changes
- Speed control
- Status monitoring
- Fault handling
- Stop method comparison

### final_system_test.py
Comprehensive system verification:
- Controller components
- Command parsing
- Speed settings
- Status display
- Overall system readiness

## Continuous Testing

For development workflow:
```bash
# Quick unit test run
python3 run_tests.py --category unit

# Full integration test when needed
python3 run_tests.py --category integration

# Complete system test before deployment
python3 run_tests.py
```

## Test Results Interpretation

✓ **PASS** - Test executed successfully  
✗ **FAIL** - Test encountered errors  
⚠ **WARNING** - Test passed with expected limitations

Some tests may show "expected connection issues" - this is normal when running without actual VFD hardware.