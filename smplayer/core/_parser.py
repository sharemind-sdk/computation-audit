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

import xml.etree.ElementTree as ET

from . import protocol as smprotocol

class LogError(Exception):

    """Raised when the parsed log file contained errors."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

"""A dict from a supported protocol tag to the corresponding protocol type."""
_supported_protocols = {
        "add": smprotocol.Addition,
        "sub": smprotocol.Subtraction,
        "mult": smprotocol.Multiplication,
        "declassify": smprotocol.Declassification,
        "sum": smprotocol.Summation,
    }

def parse_log(filename):
    """Parse a Sharemind Application Server audit log and return a tuple of protocols.

    Args:
        filename: Path to the audit log.

    Raises:
        ParseError: If the log file can't be parsed.
        LogError: If the parsed log file contains errors.

    """
    try:
        audit = ET.parse(filename).getroot()
    except ET.ParseError:
        raise LogError("XML parsing failed")

    if audit.tag != "audit":
        raise LogError("root element is not <audit>")

    protocols = []
    for protocol in audit:
        protocols.append(_parse_protocol(protocol))
    return tuple(protocols)

def _parse_protocol(protocol):
    if protocol.tag not in _supported_protocols:
        raise LogError("unknown protocol <%s>" % protocol.tag)

    input = None
    output = None
    send = {}
    recv = {}

    for block in protocol:

        if block.tag == "input":
            if input is not None:
                raise LogError("extra <input> element")
            input = _parse_vectors(block)

        elif block.tag == "output":
            if output is not None:
                raise LogError("extra <output> element")
            output = _parse_vectors(block)

        elif block.tag == "send":
            node = _get_node(block)
            if node in send:
                raise LogError("extra <send node=\"%s\"> element" % node)
            send[node] = _parse_vectors(block)

        elif block.tag == "recv":
            node = _get_node(block)
            if node in recv:
                raise LogError("extra <recv node=\"%s\"> element" % node)
            recv[node] = _parse_vectors(block)

        else:
            raise LogError("unknown block <%s>" % block.tag)

    args = [input, output]
    if len(send) > 0 or len(recv) > 0:
        # If the log contained send or receive blocks, then assume we are
        # dealing with a subclass of smprotocol.Protocol, and add these
        # blocks to the argument list. If the protocol isn't a subclass of
        # Protocol, then it will raise an exception when initializing,
        # signaling that these blocks should not be in the log.
        args.extend((send, recv))

    try:
        # Initialize a new protocol instance with the parsed arguments
        return _supported_protocols[protocol.tag](*args)
    except Exception as err:
        raise LogError("failed initializing <%s>" % protocol.tag) from err

def _get_node(block):
    if "node" not in block.attrib:
        raise LogError("<%s> element without \"node\" attribute" % block.tag)
    return block.attrib["node"]

def _parse_vectors(parent):
    vectors = []
    for vector in parent:
        vectors.append(_parse_vector(vector))

    if len(vectors) == 0:
        raise LogError("no <vector> elements found in <%s>" % parent.tag)
    elif len(vectors) == 1:
        return vectors[0]
    else:
        return tuple(vectors)

def _parse_vector(vector):
    if vector.tag != "vector":
        raise LogError("expected <vector>, but got <%s>" % s)

    values = []
    for value in vector:
        values.append(_parse_value(value))

    if len(values) == 0:
        raise LogError("empty <vector>")
    return values

def _parse_value(value):
    if value.tag != "value":
        raise LogError("expected <value>, but got <%s>" % s)

    # All values should be 32-bit unsigned integers
    try:
        integer = int(value.text)
        if integer != integer % 2**32:
            raise ValueError("value not an unsigned 32-bit integer")
        return integer
    except ValueError as err:
        raise LogError("<value> contains unsupported value") from err
