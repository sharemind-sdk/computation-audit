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
from . import _util as util

from kivy.uix.treeview import TreeViewLabel

def _format_binary(op, protocol):
    return "{a} {op} {b} = {r}".format(a=util.format_values(protocol.input[0]),
            op=op, b=util.format_values(protocol.input[1]),
            r=util.format_values(protocol.output))

def _format_function(f, protocol):
    return "{f} {v} = {r}".format(f=f, v=util.format_values(protocol.input),
            r=util.format_values(protocol.output))

# A dict from protocol type to a function that formats its header.
_protocol_headers = {
        smprotocol.Addition:         lambda p: _format_binary("+", p),
        smprotocol.Subtraction:      lambda p: _format_binary("-", p),
        smprotocol.Multiplication:   lambda p: _format_binary("*", p),
        smprotocol.Declassification: lambda p: _format_function("declassify", p),
        smprotocol.Summation:        lambda p: _format_function("sum", p),
    }

def _format_header(protocol):
    """Returns a properly formatted header for *protocol*."""
    result = protocol.result
    if isinstance(result, smprotocol.ProtocolResult):
        result = result.output
    return "{status} {label}{comment}".format(
            status=util.format_ok(protocol.verify()),
            label=_protocol_headers[type(protocol)](protocol),
            comment="" if protocol.verify() else
                    " (simulation result: {0})".format(util.format_values(result)))

class ProtocolHeader(TreeViewLabel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = _format_header(kwargs["protocol"])
