#!/usr/bin/env python3
"""Factory reset (erase flash) for ESP32 WROOM-32."""

import glob
import subprocess
import sys


def find_ports():
    ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
    return sorted(ports)


def erase_flash(port, baud=460800):
    print(f"Erasing flash on {port} at {baud} baud...")
    result = subprocess.run(
        [
            sys.executable, "-m", "esptool",
            "--chip", "esp32",
            "--port", port,
            "--baud", str(baud),
            "erase_flash",
        ],
        text=True,
    )
    return result.returncode == 0


def main():
    ports = find_ports()

    if not ports:
        print("No ESP32 port found. Plug in the device and try again.")
        print("Tip: Hold BOOT button while plugging in if auto-detect fails.")
        sys.exit(1)

    if len(ports) == 1:
        port = ports[0]
        print(f"Found port: {port}")
    else:
        print("Multiple ports found:")
        for i, p in enumerate(ports):
            print(f"  [{i}] {p}")
        idx = int(input("Select port number: "))
        port = ports[idx]

    print("\nMake sure the ESP32 is in bootloader mode:")
    print("  Hold BOOT -> press & release EN/RST -> release BOOT")
    input("Press Enter when ready...")

    success = erase_flash(port)

    if success:
        print("\nDone! Flash erased successfully.")
        print("You can now flash new firmware onto the ESP32.")
    else:
        print("\nFailed at 460800 baud, retrying at 115200...")
        success = erase_flash(port, baud=115200)
        if success:
            print("\nDone! Flash erased successfully.")
        else:
            print("\nErase failed. Check connection and try again.")
            sys.exit(1)


if __name__ == "__main__":
    main()
