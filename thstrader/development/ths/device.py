"""
Device connection management for THS Trader
Simplified version inspired by mobileas architecture
"""
import time
from functools import wraps
import uiautomator2 as u2
from PIL import Image
import numpy as np
import packaging.version


# Monkey patch to fix version parsing issue when versionName is "null"
_original_parse = packaging.version.parse


def _patched_parse(version):
    """Parse version, treating 'null' as '0.0.0'"""
    if not version or version == 'null' or version.strip() == '':
        version = '0.0.0'
    return _original_parse(version)


packaging.version.parse = _patched_parse


def retry(max_tries=3):
    """Retry decorator with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            last_exception = None
            for attempt in range(max_tries):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_tries - 1:
                        wait_time = 2 ** attempt  # exponential backoff
                        print(f"Attempt {attempt + 1} failed: {e}, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        print(f"All {max_tries} attempts failed")
            raise last_exception
        return wrapper
    return decorator


class Device:
    """
    Device connection wrapper for uiautomator2
    Handles connection initialization and provides basic operations
    """
    def __init__(self, serial):
        """
        Args:
            serial (str): Device serial like "127.0.0.1:5565"
        """
        self.serial = serial
        self._device = None
        self._connect()

    def _connect(self):
        """Initialize uiautomator2 connection"""
        print(f"Connecting to device: {self.serial}")

        # Use connect_usb for emulator/localhost connections
        # This is more stable than plain connect()
        if self.serial.startswith('emulator-') or self.serial.startswith('127.0.0.1:'):
            self._device = u2.connect_usb(self.serial)
        else:
            self._device = u2.connect(self.serial)

        # Set long timeout to keep connection alive (7 days)
        # self._device.set_new_command_timeout(604800)

        print(f"Connected to device: {self.serial}")
        # print(f"ATX Agent URL: {self._device._get_atx_agent_url()}")

    @property
    def d(self):
        """Get uiautomator2 device instance"""
        return self._device

    @retry(max_tries=3)
    def screenshot(self, filename=None):
        """
        Take a screenshot

        Args:
            filename (str, optional): File path to save screenshot

        Returns:
            PIL.Image: Screenshot image
        """
        img = self._device.screenshot()
        if filename:
            img.save(filename)
        return img

    @retry(max_tries=3)
    def click(self, x, y):
        """
        Click at coordinates

        Args:
            x (int): X coordinate
            y (int): Y coordinate
        """
        self._device.click(x, y)
        time.sleep(0.5)

    @retry(max_tries=3)
    def swipe(self, x1, y1, x2, y2, duration=0.5):
        """
        Swipe from (x1, y1) to (x2, y2)

        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates
            duration (float): Swipe duration in seconds
        """
        self._device.swipe(x1, y1, x2, y2, duration=duration)
        time.sleep(0.5)

    @retry(max_tries=3)
    def press_key(self, key):
        """
        Press a key

        Args:
            key (str): Key name like 'back', 'home', 'enter'
        """
        self._device.press(key)
        time.sleep(0.5)

    @retry(max_tries=3)
    def send_keys(self, text):
        """
        Send text input

        Args:
            text (str): Text to send
        """
        self._device.send_keys(text)
        time.sleep(0.5)

    @retry(max_tries=3)
    def app_current(self):
        """
        Get current app package name

        Returns:
            str: Package name
        """
        result = self._device.app_current()
        return result.get('package', '')

    @retry(max_tries=3)
    def app_start(self, package):
        """
        Start an app

        Args:
            package (str): Package name
        """
        self._device.app_start(package)
        time.sleep(2)

    @retry(max_tries=3)
    def app_stop(self, package):
        """
        Stop an app

        Args:
            package (str): Package name
        """
        self._device.app_stop(package)
        time.sleep(1)

    def sleep(self, seconds):
        """
        Sleep for specified seconds

        Args:
            seconds (float): Sleep duration
        """
        time.sleep(seconds)
