# pymodbus Serial Testing

A comprehensive testing suite for pymodbus serial communication with VFD (Variable Frequency Drive) devices.

## Features

- Automated serial port detection
- Enhanced error handling and logging
- Dry-run mode for testing without hardware
- Full diagnostic suite
- Support for multiple serial configurations
- Command-line interface for flexible testing

## Hardware Requirements

### USB Serial Adapters

Common USB serial adapters that work with this project:

- **FTDI adapters** (e.g., FT232R) - `/dev/ttyUSB0`
- **CP2102/CP2104** - `/dev/ttyUSB0` or `/dev/ttyACM0`
- **CH340** - `/dev/ttyUSB0`

### VFD Configuration

The default VFD configuration assumes:
- Port: `/dev/ttyUSB0`
- Baudrate: 9600
- Data bits: 8
- Stop bits: 1
- Parity: None
- Slave ID: 1

## Installation

```bash
# Activate virtual environment (if using uv)
source .venv/bin/activate

# Install dependencies (already done via pyproject.toml)
uv sync

# Optional: Install pyserial for hardware testing
pip install pyserial
```

## Permissions Setup

To access serial ports, you may need to add your user to the `dialout` group:

```bash
# Check current groups
groups

# Add user to dialout group
sudo usermod -a -G dialout $USER

# Reboot or log out and log back in for changes to take effect
```

## Quick Start

```bash
# Auto-detect serial ports and run all tests
python3 test_serial.py

# Run specific tests
python3 test_serial.py --basic          # Basic serial test
python3 test_serial.py --dry-run        # Dry-run test
python3 test_serial.py --diagnostic     # Full diagnostics
python3 test_serial.py --actual         # Actual Modbus operations
```

## Usage

### 1. Serial Port Detection

```bash
# List all available serial ports
python3 detect_serial.py

# Test a specific port
python3 detect_serial.py --port /dev/ttyUSB0 --test

# Test with specific baudrate
python3 detect_serial.py --port /dev/ttyUSB0 --test --baudrate 19200
```

### 2. Dry-Run Testing (No Hardware Required)

```bash
# Test connection parameters without hardware
python3 vfd_control.py --dry-run

# Specify custom port
python3 vfd_control.py --port /dev/ttyUSB0 --dry-run
```

### 3. Full Diagnostics

```bash
# Run comprehensive diagnostic suite
python3 serial_diagnostics.py

# Custom configuration
python3 serial_diagnostics.py --port /dev/ttyUSB0 --baudrate 9600 --slave 1
```

### 4. Actual VFD Control

```bash
# Run with default settings
python3 vfd_control.py

# Custom configuration
python3 vfd_control.py --port /dev/ttyUSB0 --baudrate 9600 --slave 1 --timeout 2
```

## Testing Workflow

### Recommended Testing Process

1. **Connect Hardware**
   ```bash
   # Plug in your USB serial adapter
   # Verify device is detected
   ls -la /dev/ttyUSB*
   ```

2. **Test Serial Connection**
   ```bash
   python3 test_serial.py --basic
   ```

3. **Run Dry-Run Test**
   ```bash
   python3 test_serial.py --dry-run
   ```

4. **Full Diagnostics**
   ```bash
   python3 test_serial.py --diagnostic
   ```

5. **Actual VFD Operations** 
   ```bash
   python3 test_serial.py --actual
   ```

## Script Descriptions

### `vfd_control.py`
Enhanced VFD control script with:
- Command-line argument support
- Error handling and logging
- Dry-run mode
- Connection verification

### `detect_serial.py`
Serial port detection utility:
- Auto-detects all available serial ports
- Checks port accessibility and permissions
- Tests basic serial communication
- Provides user-friendly error messages

### `serial_diagnostics.py`
Comprehensive diagnostic suite:
- Connection parameter validation
- Serial connection testing
- Register read/write operations
- Exception handling verification
- Detailed test results

### `test_serial.py`
Automated test runner:
- Comprehensive test automation
- Sequential test execution
- User-friendly interface
- Configurable parameters
- Test result aggregation

## Troubleshooting

### No Serial Ports Found

```bash
# Check if device is connected
lsusb | grep -i serial

# Check dmesg for USB device information
dmesg | tail -20

# Try running as root to check if device is detected
sudo python3 detect_serial.py
```

### Permission Denied

```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Check current permissions
ls -la /dev/ttyUSB0

# Test with sudo (temporary fix)
sudo python3 test_serial.py --basic
```

### Connection Timeout

```bash
# Increase timeout value
python3 vfd_control.py --port /dev/ttyUSB0 --timeout 5

# Check serial cable connections
# Verify VFD is powered on and in serial mode
# Confirm baudrate matches VFD settings
```

### Modbus Errors

```bash
# Run diagnostics for detailed error information
python3 serial_diagnostics.py --port /dev/ttyUSB0

# Check VFD slave ID matches configuration
python3 vfd_control.py --slave 2  # Try different slave ID
```

## Advanced Configuration

### Custom Baudrates

```bash
# Common baudrates: 9600, 19200, 38400, 57600, 115200
python3 vfd_control.py --baudrate 19200
```

### Multiple VFD Support

```bash
# Control different VFDs with different slave IDs
python3 vfd_control.py --slave 2 --port /dev/ttyUSB0
python3 vfd_control.py --slave 1 --port /dev/ttyUSB1
```

### Logging Configuration

The scripts use Python's logging module. To increase verbosity:

```python
# Modify the logging level in any script
logging.basicConfig(level=logging.DEBUG)  # More detailed logging
```

## VFD Control (T9000/9400 Series)

### VFD Controller Files

The project includes specialized VFD control files for the T9000/9400 series Variable Frequency Drives:

- **vfd_test_controller.py** - Main VFD control class with all basic commands
- **vfd_basic_commands.py** - Comprehensive test suite with multiple test scenarios
- **vfd_test_setup.py** - Setup verification and controller testing
- **vfd_control.py** - Original VFD control script (enhanced version with error handling)

### VFD Command Reference

#### Basic Motor Control Commands

| Command | Description | Register Value |
|---------|-------------|----------------|
| `start_forward(speed%)` | Start motor in forward direction | 0x2000 = 1 |
| `start_reverse(speed%)` | Start motor in reverse direction | 0x2000 = 2 |
| `coast_stop()` | Immediate stop (no deceleration) | 0x2000 = 5 |
| `ramp_stop()` | Stop with deceleration | 0x2000 = 6 |
| `fault_reset()` | Reset VFD faults | 0x2000 = 7 |

#### Speed Control

| Command | Description | Range |
|---------|-------------|-------|
| `set_speed_percent(0-100)` | Set speed as percentage of max | 0-100% |
| `set_frequency_hz(0-50)` | Set specific frequency | 0-50Hz |

**Speed Scaling Formula:**  
`frequency_value = (percentage / 100) * 10000`

Examples:
- 25% = 2500 (12.5Hz at 50Hz max)
- 50% = 5000 (25Hz at 50Hz max)  
- 100% = 10000 (50Hz at 50Hz max)

#### Status Monitoring

| Command | Description |
|---------|-------------|
| `get_status()` | Read complete status (running, direction, fault) |
| `is_running()` | Check if motor is running |
| `has_fault()` | Check if VFD has active fault |
| `get_fault_code()` | Get current fault code |
| `get_comm_fault()` | Get communication fault code |

**Status Register (0x3000) Bit Definitions:**
- Bit 0: Running (1 = motor is running)
- Bit 1: Reverse (1 = running in reverse)
- Bit 2: Fault (1 = fault condition active)

### VFD Communication Setup

#### Required VFD Parameters

```text
P0.02 = 2    # Command source = communication
P0.03 = 9    # Frequency source = communication
```

#### RS485 Wiring

```
VFD RS+ → RS485 A / D+
VFD RS- → RS485 B / D-
VFD GND → Adapter GND (optional but recommended)
```

#### Communication Parameters

- **Protocol:** Modbus RTU
- **Baudrate:** 9600
- **Databits:** 8
- **Parity:** None
- **Stopbits:** 1
- **Slave ID:** 1 (configurable)

### VFD Controller Usage

#### Basic Example

```python
from vfd_test_controller import VFDTestController

# Create controller instance
controller = VFDTestController(port='/dev/ttyUSB0')

# Connect to VFD
controller.connect()

# Start forward at 25% speed
controller.start_forward(25)

# Check status
status = controller.get_status()
print(f"Running: {status['running']}")

# Stop with deceleration
controller.ramp_stop()

# Disconnect
controller.disconnect()
```

#### Interactive Usage

```bash
# Run interactive controller
python3 vfd_test_controller.py

# Read status only
python3 vfd_test_controller.py --status

# With custom parameters
python3 vfd_test_controller.py --port /dev/ttyUSB0 --slave 1
```

### VFD Test Suite

#### Running Tests

```bash
# Run all tests
python3 vfd_basic_commands.py --test all

# Run specific test
python3 vfd_basic_commands.py --test start_stop
python3 vfd_basic_commands.py --test direction
python3 vfd_basic_commands.py --test speed
python3 vfd_basic_commands.py --test monitor
python3 vfd_basic_commands.py --test fault
python3 vfd_basic_commands.py --test stop

# With custom port
python3 vfd_basic_commands.py --port /dev/ttyUSB0 --test all
```

#### Available Tests

| Test | Description |
|------|-------------|
| `start_stop` | Basic forward start/stop with status checks |
| `direction` | Forward → Reverse direction change |
| `speed` | Speed control using percentage and frequency |
| `monitor` | Status monitoring and fault detection |
| `fault` | Fault detection and reset procedures |
| `stop` | Comparison of ramp stop vs coast stop |
| `all` | Run all tests sequentially |

#### Test Output Example

```
============================================================
TEST 1: Basic Start/Stop (Forward)
============================================================

1. Starting VFD forward at 25% speed...
✓ Write successful: 0x2000 = 1

2. Stopping VFD with ramp stop...
✓ Write successful: 0x2000 = 6

✓ Basic Start/Stop: PASSED
```

#### Quick VFD Test Workflow

```bash
# 1. Verify controller setup
python3 vfd_test_setup.py

# 2. Check VFD connectivity
python3 vfd_test_controller.py --status

# 3. Run basic start/stop test
python3 vfd_basic_commands.py --test start_stop

# 4. Run comprehensive test suite
python3 vfd_basic_commands.py --test all

# 5. Try interactive keyboard control (NEW!)
python3 vfd_interactive.py
```

## Interactive VFD Control (NEW!)

### Keyboard-Based VFD Control

The `vfd_interactive.py` script provides real-time keyboard control with live status display.

#### Starting Interactive Control

```bash
# Start with default settings
python3 vfd_interactive.py

# With custom parameters
python3 vfd_interactive.py --port /dev/ttyUSB0 --baudrate 9600

# Custom speed range and increments
python3 vfd_interactive.py --min-speed 5 --max-speed 80 --speed-step 10
```

#### Keyboard Controls

| Key | Action | Description |
|-----|--------|-------------|
| `SPACE` | Start/Stop | Toggle motor running state |
| `LEFT` | Reverse | Change direction to REVERSE |
| `RIGHT` | Forward | Change direction to FORWARD |
| `UP` | Speed+ | Increase speed by 5% |
| `DOWN` | Speed- | Decrease speed by 5% |
| `0-9` | Set Speed | Set speed (e.g., 5=50%, 0=100%) |
| `r` | Reset | Reset VFD fault |
| `s` | Status | Show detailed VFD status |
| `e` | Emergency | Immediate emergency stop |
| `q` | Quit | Exit application |

#### Real-Time Status Display

The interactive interface shows:

```
============================================================
       VFD INTERACTIVE CONTROL - FORWARD
============================================================

📊 STATUS:
   Running:  ✓ RUNNING
   Direction: → FORWARD
   Target Speed: 50%
   Actual Speed: 50%

🔧 VFD REAL-TIME:
   Status: RUNNING
   Direction: FORWARD
   Fault: OK

⌨️  CONTROLS:
   [SPACE]     Start/Stop motor
   [LEFT]      Reverse direction  
   [RIGHT]     Forward direction
   [UP]        Increase speed (+5%)
   [DOWN]      Decrease speed (-5%)
   [0-9]       Set speed (e.g., 5 = 50%, 0 = 100%)
   [r]         Reset fault
   [s]         Show VFD status
   [e]         Emergency stop
   [q]         Quit

============================================================
```

#### Usage Example

```bash
$ python3 vfd_interactive.py

============================================================
   VFD INTERACTIVE CONTROL SYSTEM
============================================================

Connected to VFD on /dev/ttyUSB0

⚙️  Settings:
   Port: /dev/ttyUSB0
   Baudrate: 9600
   Slave ID: 1
   Speed Range: 5% - 100%
   Speed Step: 5%

🎮 Starting interactive control...

> space
▶️  Starting motor...

> 2
🎚️  Speed set to: 20%

> up
⬆️  Speed increased: 20% → 25%

> left
🔄 Direction changed: FORWARD → REVERSE

> space
🛑 Stopping motor...

> q
👋 Quitting interactive control...
```

#### Interactive Features

- **Real-time status updates** after each command
- **Direction change** with automatic motor restart
- **Speed control** with gradual increments/decrements
- **Quick speed setting** via number keys (5=50%, 0=100%)
- **Fault monitoring** and reset capabilities
- **Emergency stop** for immediate halt
- **Safety checks** before motor operations

#### Running Demo

```bash
# Run interactive demo (simulated - no hardware needed)
python3 demo_vfd_interactive.py
```

This demonstrates the interface behavior before connecting actual VFD hardware.

### VFD Parameter Configuration

Ensure your VFD is configured for serial control:

```text
P0.00 = 1.0          # Command source selection
P0.02 = 2            # Communication command source
P0.03 = 9            # Communication frequency source
P0.04 = 9600         # Communication baud rate
P0.05 = 1            # Communication slave ID
P0.07 = 10000        # Frequency word length
P0.08 = 1            # Communication data bits
```

### Troubleshooting VFD Issues

#### VFD Not Responding
```bash
# Check connectivity
python3 vfd_test_controller.py --status

# Verify VFD parameters match communication settings
# Check RS485 wiring connections
```

#### VFD Has Fault
```python
# Check fault code
controller.get_fault_code()

# Reset fault
controller.fault_reset()
```

#### Motor Not Starting
```python
# Check VFD parameters P0.02 and P0.03
# Verify status register shows ready state
# Test with manual mode first to ensure motor/VFD working
# Check for safety interlocks or emergency stop
```

#### Speed Not Changing
```python
# Verify frequency source is communication (P0.03 = 9)
# Check speed control register writes are successful
# Test with frequency commands vs percentage commands
```

## Modbus Register Map (T9000/9400 VFD)

| Address | Access | Function | Description |
|---------|--------|----------|-------------|
| 0x1000  | Write  | Speed Setting | Frequency command (0-10000 = 0-100%) |
| 0x2000  | Write  | Control Command | 1=Forward, 2=Reverse, 5=Coast Stop, 6=Ramp Stop, 7=Fault Reset |
| 0x3000  | Read   | Status Register | Bit0=Running, Bit1=Reverse, Bit2=Fault |
| 0x8000  | Read   | Fault Code | Current fault code |
| 0x8001  | Read   | Comm Fault | Communication fault code |

## Safety Precautions

⚠️ **Important Safety Notes:**

- Always test with dry-run mode first
- Use proper VFD隔离来防止高压危险
- Ensure VFD is properly configured for serial control
- Start with low-speed tests before full operation
- Have emergency stop procedures in place

License: MIT