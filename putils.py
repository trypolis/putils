# Putils
# Single-file Python library of functions.
#
# Copyright (C) 2020, Ty Gillespie. All rights reserved.
# MIT Licensed. See the LICENSE file more spacific
# licencing terms.

import sys


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
