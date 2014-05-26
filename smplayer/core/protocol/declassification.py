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

import functools

from . import protocol
from .. import _util as util

class Declassification(protocol.Protocol):

    """SMC declassification protocol."""

    def __init__(self, input, output, send, recv, context=None):
        """Instantiate a new declassification protocol block with the given attributes.

        The input list, the output list and all lists sent or received as
        messages must have the same length and contain 32-bit integers.

        Args:
            input: A list of integers to declassify.

            output: The list of declassified integers.

            send: A map containing messages sent to other nodes. Must contain
                keys "next" and "remote" which map to messages sent to the next
                node and all remote nodes, respectively. Both keys must map to
                a single message, i.e. a list of integers.

            recv: A map containing messages received from other nodes. Must
                contain keys "prev" and "computing" which map to messages
                received received from the previous node and all computing
                nodes, respectively. The single message in "prev" is not
                duplicated in "computing" even though the previous node is also
                a computing node. "prev" must map to a single message and
                "computing" must contain as many messages as there are
                computing nodes (context.computing) minus one.

            context: The context to use for simulation. A default is used if None.

        Raises:
            ValueError: If any ony of the lists are of invalid length.
            KeyError: If any of the expected keys in *send* or *recv* are
                missing, or if there are any extra ones.

        """
        super().__init__(input, output, send, recv, context)

        n = len(self.input)
        util.check_len(self.output, n, "output")

        self._send_remote = self.send["remote"]
        util.check_len(self._send_remote, n, "send['remote']")

        self._send_next = self.send["next"]
        util.check_len(self._send_next, n, "send['next']")

        self._recv_prev = self.recv["prev"]
        util.check_len(self._recv_prev, n, "recv['prev']")

        self._recv_computing = self.recv["computing"]
        util.check_len(self._recv_computing, self.context.computing - 1, "recv['computing']")
        util.check_all_len(self._recv_computing, n, "recv['computing']")

        util.check_keys(self.send, { "next", "remote" }, "send")
        util.check_keys(self.recv, { "prev", "computing" }, "recv")

    def _simulate(self):
        """Simulate the declassification protocol with the input attributes."""
        mod = self.context.mod # Use a shorter alias.

        # The next node is sent a list of random values, so just use the random
        # values given in the _send_next attribute.
        vec_sn = self._send_next

        # Reshare the input using the random values received from the previous
        # node and sent to next one. Send the result to all remote nodes.
        vec_sr = [(x + rp - r) % mod
                for (x, rp, r) in zip(self.input, self._recv_prev, vec_sn)]

        # Receive all the shares sent by other computing nodes and combine them
        # with our own share.

        # Use a separate helper function instead of a lambda to improve readability.
        def sum_vec(vec_x, vec_y):
            """Sums two lists elementwise."""
            return [(x + y) % mod for (x, y) in zip(vec_x, vec_y)]

        vec_out = functools.reduce(sum_vec, self._recv_computing, vec_sr)

        return protocol.ProtocolResult(vec_out, { "next": vec_sn, "remote": vec_sr }, None)
