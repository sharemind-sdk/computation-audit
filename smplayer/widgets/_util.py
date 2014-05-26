#!/usr/bin/env python3

"""
Copyright (c) 2014, Cybernetica AS, STACC
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

from ..core import protocol as smprotocol

def int_to_color(value):
    """Converts an integer to a color code that corresponds to it.

    Returns a colorcode between 0x555555 and 0xffffff. The string contains the
    hexadecimal value, but without a leading '0x'.

    """
    # Use a random odd constant (0xe170e5) to ensure that small differences
    # cause noticeably different colors.
    color = 0x555555 + (0xe170e5 * value % 0xaaaaab)
    return hex(color)[2:] # Strip '0x' from the hex representation.

def format_value(value, color=None):
    """Formats a single value in markup."""
    color = color or int_to_color(value)
    return "[color=#{color}][i]{value}[/i][/color]".format(color=color, value=value)

def format_values(values):
    """Formats either a single value or a list of values in markup."""
    if hasattr(values, "__iter__"):
        return "&bl;{0}&br;".format(", ".join(map(format_value, values)))
    return format_value(values)

def format_ok(ok):
    """Format the given boolean as a colored "ok" or "FAIL"."""
    return "[color=#55ff55]ok[/color]" if ok else "[color=#ff5555]FAIL[/color]"
