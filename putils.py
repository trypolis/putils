# Putils
# Single-file Python library of functions.
#
# Copyright (C) 2020, Ty Gillespie. All rights reserved.
# MIT Licensed. See the LICENSE file more spacific
# licencing terms.

import sys
import platform
import ctypes
import os
import signal


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


def kill_windows_process(pid):
    """Kill a Windows process."""
    PROCESS_TERMINATE = 1
    SYNCHRONIZE = 1048576
    handle = ctypes.windll.kernel32.OpenProcess(
        PROCESS_TERMINATE | SYNCHRONIZE, False, pid
    )
    ctypes.windll.kernel32.TerminateProcess(handle, -1)
    ctypes.windll.kernel32.WaitForSingleObject(handle, 1000)
    ctypes.windll.kernel32.CloseHandle(handle)


def kill_unix_process(pid):
    """Kills a process on Unix systems, such as Mac or Linux."""
    try:
        os.kill(pid, signal.SIGKILL)
    except OSError:
        pass


def kill_process(pid):
    """Forcefully kills a process."""
    if pid < 0:
        return
    if platform.system() == "Windows":
        kill_windows_process(pid)
    else:
        kill_unix_process(pid)
