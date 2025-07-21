# Matrix Automation CLI

Matrix Automation CLI is a command-line tool for simulating user activity on Instagram and Threads apps. It supports multi-device automation via ADB and is ideal for behavior testing, account warming, content farming, and user flow simulation.

## Features

* 🔍 Scan connected Android devices and export device info
* 🤖 Simulate Instagram home feed browsing
* 🧵 Simulate Threads home feed browsing

---

## Installation

We recommend running this project inside a virtual environment.

```
git clone https://github.com/your-org/matrix-automation-cli.git
cd matrix-automation-cli
pip install -r requirements.txt
```

---

## Usage

Run the CLI with the following format:

```
python cli.py <command> [options]
```

---

## Commands and Options

### 1. Device Management

Scan connected Android devices and export their details to a CSV file.

```
python cli.py device --mode scan --path <ADB_PATH> --file <OUTPUT_CSV>
```

Options:

* `--mode`: Mode of operation (currently only `scan`)
* `--path`: Path to ADB binary (e.g., `/usr/bin/adb`)
* `--file`: Output CSV filename

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