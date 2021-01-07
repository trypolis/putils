# Putils
# Single-file Python library of functions.
#
# Copyright (C) 2020, Ty Gillespie. All rights reserved.
# MIT Licensed. See the LICENSE file more spacific
# licencing terms.

"""Process killing functions."""

import platform
import ctypes
import os
import signal


def kill_windows_process(pid: int):
    """Kill a Windows process."""
    PROCESS_TERMINATE: int = 1
    SYNCHRONIZE: int = 1048576
    handle = ctypes.windll.kernel32.OpenProcess(
        PROCESS_TERMINATE | SYNCHRONIZE, False, pid
    )
    ctypes.windll.kernel32.TerminateProcess(handle, -1)
    ctypes.windll.kernel32.WaitForSingleObject(handle, 1000)
    ctypes.windll.kernel32.CloseHandle(handle)


def kill_unix_process(pid: int):
    """Kills a process on Unix systems, such as Mac or Linux."""
    try:
        os.kill(pid, signal.SIGKILL)
    except OSError:
        pass


def kill_process(pid: int) -> bool:
    """Forcefully kills a process."""
    if pid < 0:
        return False
    if platform.system() == "Windows":
        kill_windows_process(pid)
    else:
        kill_unix_process(pid)
    return True


system: str = platform.system()


def get_user_idle_time() -> int:
    """
    Return the amount of time (in seconds) that the user is said to be idle.
    This is normally obtained from a lack of keyboard and/or mouse input.
    """
    if system == "Windows":
        return get_user_idle_time_windows()
    elif system == "Darwin":
        return get_user_idle_time_mac()
    raise NotImplementedError("This function is not yet implemented for %s" % system)


def get_user_idle_time_windows() -> int:
    from ctypes import Structure, windll, c_uint, sizeof, byref

    class LASTINPUTINFO(Structure):
        _fields_ = [("cbSize", c_uint), ("dwTime", c_uint)]

    lastInputInfo: LASTINPUTINFO = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis: int = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0


def get_user_idle_time_mac() -> int:
    import subprocess
    import re

    s = subprocess.Popen(("ioreg", "-c", "IOHIDSystem"), stdout=subprocess.PIPE)
    data = s.communicate()[0]
    expression = "HIDIdleTime.*"
    try:
        data = data.decode()
        r = re.compile(expression)
    except UnicodeDecodeError:
        r = re.compile(expression.encode())
    return int(r.findall(data)[0].split(" = ")[1]) / 1000000000
