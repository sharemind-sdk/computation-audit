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

from . import protocol
from .. import _util as util

import collections

class MultiplicationSimulation(collections.namedtuple("MultiplicationSimulation",
        "vec_a vec_b vec_ap vec_bp vec_rp")):
    __slots__ = ()
    """Information needed to trace a multiplication protocol simulation.

    Attributes:
        vec_a: Reshared value of the first input parameter.
        vec_b: Reshared value of the second input parameter.
        vec_ap: Reshared value of the first input parameter of the previous node.
        vec_bp: Reshared value of the second input parameter of the previous node.
        vec_rp: Randomness used to reshare the output.

    """

class Multiplication(protocol.Protocol):

    """SMC multiplication protocol."""

    def __init__(self, input, output, send, recv, context=None):
        """Instantiate a new multiplication protocol block with the given attributes.

        The input lists, the output list and all lists sent or received as
        messages must have the same length and contain 32-bit integers.

        Args:
            input: A pair of lists of integers to be multiplied elementwise.

            output: The expected result of multiplying the input lists together.

            send: A map containing messages sent to other nodes. Must contain
                keys "next" and "prev" which map to lists of messages sent to
                the next and previous computing node, respectively. "next" must
                contain 3 messages and "prev" must contain 2 messages.

            recv: A map containing messages received from other nodes. Must
                contain keys "next" and "prev" which map to lists of messages
                received received from the next and previous computing node,
                respectively. "next" must contain 2 messages and "prev" must
                contain 3 messages.

            context: The context to use for simulation. A default is used if None.

        Raises:
            ValueError: If any ony of the lists are of invalid length.
            KeyError: If *send* or *recv* don't have keys "next" and "prev" or
                if they contain any extra keys.

        """
        super().__init__(input, output, send, recv, context)

        # prefer using self.input, because Protocol.__init__ might have
        # modified it. The same goes for all other attributes.
        util.check_len(self.input, 2, "input")
        self._vec_a = self.input[0]
        self._vec_b = self.input[1]

        n = len(self._vec_a)
        if len(self._vec_b) != n:
            raise ValueError("The lists in input must have equal length")

        util.check_len(self.output, n, "output")

        self._send_prev = self.send["prev"]
        util.check_len(self._send_prev, 2, "send['prev']")
        util.check_all_len(self._send_prev, n, "send['prev']")

        self._send_next = self.send["next"]
        util.check_len(self._send_next, 3, "send['next']")
        util.check_all_len(self._send_next, n, "send['next']")

        self._recv_prev = self.recv["prev"]
        util.check_len(self._recv_prev, 3, "recv['prev']")
        util.check_all_len(self._recv_prev, n, "recv['prev']")

        self._recv_next = self.recv["next"]
        util.check_len(self._recv_next, 2, "recv['next']")
        util.check_all_len(self._recv_next, n, "recv['next']")

        expected = { "next", "prev" }
        util.check_keys(self.send, expected, "send")
        util.check_keys(self.recv, expected, "recv")

    def _simulate(self):
        """Simulate the multiplication protocol with the input attributes."""
        mod = self.context.mod # Use a shorter alias.

        # The previous node is sent 2 lists of random integers, so just use
        # the random values given in the _send_prev attribute.
        vec_sp = self._send_prev

        # The next node is sent 3 lists of integers:
        # - _vec_a with the first list of vec_sp subtracted from it elementwise.
        # - _vec_b with the second list of vec_sp subtracted from it elementwise.
        # - a list of random integers given as the third list of the _send_next attribute.
        vec_sn = ([(a - r) % mod for (a, r) in zip(self._vec_a, vec_sp[0])],
                  [(b - r) % mod for (b, r) in zip(self._vec_b, vec_sp[1])],
                  self._send_next[2])

        # Add the received random values to complete resharing of _vec_a and _vec_b.
        vec_a = [(a + r) % mod for (a, r) in zip(vec_sn[0], self._recv_next[0])]
        vec_b = [(b + r) % mod for (b, r) in zip(vec_sn[1], self._recv_next[1])]

        # Complete resharing the values received from the previous node.
        vec_ap = [(ap + r) % mod for (ap, r) in zip(self._recv_prev[0], vec_sp[0])]
        vec_bp = [(bp + r) % mod for (bp, r) in zip(self._recv_prev[1], vec_sp[1])]
        vec_rp = [(r - rp) % mod for (r, rp) in zip(vec_sn[2], self._recv_prev[2])]

        # Do the share multiplication and resharing.
        vec_out = [(a*b + a*bp + ap*b + r) % mod
                for (a, b, ap, bp, r) in zip(vec_a, vec_b, vec_ap, vec_bp, vec_rp)]

        return protocol.ProtocolResult(vec_out, { "prev": vec_sp, "next": vec_sn },
                MultiplicationSimulation(vec_a, vec_b, vec_ap, vec_bp, vec_rp))
