# Matrix Automation CLI

Matrix Automation CLI is a command-line tool for simulating user activity on Instagram and Threads apps. It supports multi-device automation via ADB and is ideal for behavior testing, account warming, content farming, and user flow simulation.

## Features

* 🔍 Scan connected Android devices and export device info
* 🤖 Simulate Instagram home feed browsing
* 🧵 Simulate Threads home feed browsing

---

## Installation

### System Requirements

* Python 3.7 or higher
* Android Debug Bridge (ADB)
* Android devices with USB debugging enabled
* macOS, Linux, or Windows

### ADB Installation

**macOS (using Homebrew):**
```bash
brew install android-platform-tools
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install android-tools-adb
```

**Windows:**
Download Android SDK Platform Tools from the official Android developer website.

### Project Setup

We recommend running this project inside a virtual environment.

```bash
# Clone the repository
git clone https://github.com/your-org/matrix-automation-cli.git
cd matrix-automation-cli

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirement.txt
```

---

## Key Dependencies

This project relies on several key libraries:

* **adbutils** (2.9.3) - Android Debug Bridge utilities for device communication
* **uiautomator2** (3.3.3) - UI automation framework for Android devices
* **click** (8.2.1) - Command-line interface creation toolkit
* **construct** (2.10.70) - Binary data structure parsing and building
* **pillow** (11.3.0) - Image processing capabilities
* **fastapi** (0.115.12) - Modern web framework for building APIs
* **uvicorn** (0.35.0) - ASGI server implementation

For a complete list of dependencies, see <mcfile name="requirement.txt" path="/Users/shinyui/Code/Matrix-Automation-Cli/requirement.txt"></mcfile>.

---

## Usage

Run the CLI with the following format:

```
python cli.py <command> [options]
```

---

## Commands and Options

### 1. Device Management

#### Scan Devices

Scan connected Android devices and export their details to a CSV file.

```
python cli.py device --mode scan --path <ADB_PATH> --file <OUTPUT_CSV>
```

#### Initialize Device Folders

Create device-specific folders for organizing automation data.

```
python cli.py device --mode init --path <ADB_PATH> --folders <ROOT_PATH>
```

Options:

* `--mode`: Mode of operation (`scan` or `init`)
* `--path`: Path to ADB binary (e.g., `/usr/bin/adb`)
* `--file`: Output CSV filename (for scan mode)
* `--folders`: Root path for creating device folders (for init mode)

---

### 2. Instagram Simulation

Simulate user behavior in the Instagram app (currently supports home feed).

```
python cli.py instagram --mode home --device <DEVICE_CSV> --step 100
```

Options:

* `--mode`: Simulation mode: `home` or `reels`
* `--device`: Path to device CSV file
* `--step`: Number of simulation steps (default: 100)

---

### 3. Threads Simulation

Simulate user behavior in the Threads app (currently supports home feed).

```
python cli.py threads --mode home --device <DEVICE_CSV> --step 100
```

Options:

* `--mode`: Simulation mode: `home` or `reels`
* `--device`: Path to device CSV file
* `--step`: Number of simulation steps (default: 100)

---

## Example Workflow

1. Scan devices and save info:

```
python cli.py device --mode scan --path /usr/local/bin/adb --file devices.csv
```

2. Simulate Instagram home feed:

```
python cli.py instagram --mode home --device devices.csv --step 200
```

3. Simulate Threads home feed:

```
python cli.py threads --mode home --device devices.csv --step 150
```

---

## Project Structure

```
Matrix-Automation-Cli/
├── cli.py                      # Main CLI entry point
├── requirement.txt             # Project dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── instagram/                  # Instagram automation modules
│   └── simulate_home_activity/
│       ├── __init__.py
│       ├── comments.txt        # Sample comments for interactions
│       ├── concurrent_runner.py # Multi-device runner
│       ├── markov_walk.py      # Markov chain behavior simulation
│       ├── state_to_back_steps.py # Navigation state management
│       └── states.py           # App state definitions
├── threads/                    # Threads automation modules
│   └── simulate_home_activity/
│       ├── __init__.py
│       ├── comments.txt        # Sample comments for interactions
│       ├── concurrent_runner.py # Multi-device runner
│       ├── markov_walk.py      # Markov chain behavior simulation
│       ├── state_to_back_steps.py # Navigation state management
│       └── states.py           # App state definitions
└── utils/                      # Shared utility modules
    ├── click.py                # Click/tap utilities
    ├── comments.txt            # Global comment templates
    ├── device.py               # ADB device management
    ├── go_back.py              # Navigation utilities
    ├── parse_comment.py        # Comment parsing utilities
    ├── post_comment.py         # Comment posting utilities
    └── swipe.py                # Swipe gesture utilities
```

---

## Device CSV Format

The scanned output is saved as a CSV file in the following format:

```
serial,ip
RTZ16888,192.0.0.168
...
```

---

## Notes

* Make sure your devices are connected via USB or ADB over network, and USB debugging is enabled.
* ADB (Android Debug Bridge) must be installed.
* Simulation behavior is based on an internal Markov chain model. Please use responsibly and do not violate platform policies.