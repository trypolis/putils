# Putils
# Single-file Python library of functions.
#
# Copyright (C) 2020, Ty Gillespie. All rights reserved.
# MIT Licensed. See the LICENSE file more spacific
# licencing terms.

import sys
import ctypes
import threading


# DLL Handles.
kernel32 = ctypes.windll.kernel32


def log_tracebacks(log_file: str, append: bool = True) -> bool:
    """Logs any tracebacks to sys.stderr."""
    if append:
        temp_file: file = open(log_file, "a")
    else:
        temp_file: file = open(log_file, "w")
    if temp_file is None:
        return False
    sys.stderr = temp_file
    return True


def beep(frequency: int, length: int, threaded: bool = False) -> bool:
    """Beeps to the PC Speaker."""
    if threaded:
        beep_thread: threading.Thread = threading.Thread(
            target=lambda: kernel32.Beep(frequency, length)
        )
        if beep_thread is None:
            return False
        beep_thread.start()
        return True
    else:
        kernel32.Beep(frequency, length)
        return True
