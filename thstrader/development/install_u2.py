#!/usr/bin/env python3
"""
Install uiautomator2 on the device properly
"""
import uiautomator2 as u2
import uiautomator2.init as u2init
from adbutils import AdbClient, AdbDevice
import logging

serial = "127.0.0.1:5565"

print(f"Installing uiautomator2 on {serial}...")
print("This may take a few minutes...")

try:
    # Set up logging to see what's happening
    logging.basicConfig(level=logging.INFO)

    # Create ADB client and device (needed for installer)
    adb_client = AdbClient(host="127.0.0.1", port=5037)
    adb_device = AdbDevice(adb_client, serial)

    # Create installer with ADB device
    print("\nCreating installer...")
    installer = u2init.Initer(adb_device, loglevel=logging.INFO)

    # Fix for MuMu emulator - check if abi is valid
    if installer.abi not in ['x86_64', 'x86', 'arm64-v8a', 'armeabi-v7a', 'armeabi']:
        print(f"Invalid ABI '{installer.abi}', using first available: {installer.abis[0]}")
        installer.abi = installer.abis[0]

    # Set ATX agent address
    installer.set_atx_agent_addr('127.0.0.1:7912')

    # Install
    print("\nStarting installation...")
    try:
        installer.install()
    except ConnectionError:
        print("Using fallback mirror...")
        u2init.GITHUB_BASEURL = 'http://tool.appetizer.io/openatx'
        installer.install()

    print("\n✓ Installation complete!")

    # Remove minicap (it can cause issues)
    print("\nRemoving minicap...")
    adb_device.shell(["rm", "-f", "/data/local/tmp/minicap"])
    adb_device.shell(["rm", "-f", "/data/local/tmp/minicap.so"])

    print("\nTesting connection...")
    # Test the connection with u2
    d = u2.connect_usb(serial)
    d.set_new_command_timeout(604800)
    info = d.info
    print(f"Device info: {info}")
    print("\n✓ Everything works!")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
