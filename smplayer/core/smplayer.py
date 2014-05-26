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

import collections
import hashlib
import base64

from . import _parser as parser
from . import protocol as smprotocol

class _sha256(object):
    """Internal private wrapper around hashlib.sha256."""

    def __init__(self):
        self._digest = hashlib.sha256()
        self._updated = False

    def update(self, value):
        if value != None:
            self._digest.update(str(value).encode())
            self._updated = True

    def digest(self):
        return base64.b64encode(self._digest.digest()).decode() if self._updated else None

class MessageHash(collections.namedtuple("MessageHash",
        "send_prev send_next send_remote recv_prev recv_next recv_computing")):
    __slots__ = ()
    """Contains hashes of sent and received messages grouped by recipient/sender.

    Attributes:
        send_prev: A hash of all messages sent to the previous node.
        send_next: A hash of all messages sent to the next node.
        send_remote: A hash of all messages sent to all remote nodes.
        recv_prev: A hash of all messages received from the previous node.
        recv_next: A hash of all messages received from the next node.
        recv_computing: A list of hashed messages received from remote
            computing nodes.

    """

class SMPlayer(object):

    """Sharemind Player class, which simulates protocols read from Sharemind
    Application Servers and verifies that the protocols were executed correctly
    (i.e. the simulation yields the same results).

    Attributes:
        protocols: A tuple containing the protocols parsed from the log. Used
            to find out why verification failed. None if no file is opened.

    """

    def __init__(self):
        self.protocols = None

    def open(self, filename):
        """Opens a Sharemind Application Server audit log.

        See smplayer._parser.parse_log for more details.

        """
        self.protocols = parser.parse_log(filename)

    def verify(self):
        """Verify the chain of protocols read from the audit log.

        If no protocols are present, returns True.

        """
        if self.protocols:
            return all(map(lambda p: p.verify(), self.protocols))
        return True

    def hash(self):
        """Returns the hashes of all sent and received messages in a MessageHash.

        These hashes can be compared with hashes computed from other audit logs
        to verify that no messages were modified.

        The hash function used is SHA-256.

        """
        if not self.protocols:
            return None

        send_prev = _sha256()
        send_next = _sha256()
        send_remote = _sha256()
        recv_prev = _sha256()
        recv_next = _sha256()
        recv_computing = []

        for protocol in self.protocols:
            if not isinstance(protocol, smprotocol.Protocol):
                # Ignore smprotocol.Blocks that don't send messages.
                continue

            # use dict.get(key) instead of dict[key] to avoid KeyErrors.
            if protocol.send:
                send_prev.update(protocol.send.get("prev"))
                send_next.update(protocol.send.get("next"))
                send_remote.update(protocol.send.get("remote"))

            if protocol.recv:
                recv_prev.update(protocol.recv.get("prev"))
                recv_next.update(protocol.recv.get("next"))
                if "computing" in protocol.recv:
                    for i in range(0, len(protocol.recv["computing"])):
                        if len(recv_computing) <= i:
                            recv_computing.append(_sha256())
                        recv_computing[i].update(protocol.recv["computing"][i])


        return MessageHash(send_prev.digest(), send_next.digest(), send_remote.digest(),
                recv_prev.digest(), recv_next.digest(),
                list(map(lambda sha: sha.digest(), recv_computing)))
