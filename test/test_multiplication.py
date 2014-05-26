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

import unittest

import smplayer.core.protocol as protocol

class TestMultiplicationProtocol(unittest.TestCase):

    def setUp(self):
        input = ([3558600623, 3558600623], [1212808259, 1212808259])
        output = [258869064, 705329063]
        send = { "prev": ([1188854041, 3234521961], [1094777806, 3747098172]),
                 "next": ([2369746582, 324078662], [118030453, 1760677383], [906647650, 3720865909]) }
        recv = { "prev": ([3159099370, 932751163], [1949237514, 1785034127], [3890975704, 308914436]),
                 "next": ([3715195981, 2305937676], [815921476, 1515753921]) }

        self._mult = protocol.Multiplication( \
                input, output, send, recv)

    def test_verify(self):
        self.assertTrue(self._mult.verify(), "Verification failed: " \
                "expected {0}, but got {1}".format( \
                    protocol.ProtocolResult(self._mult.output, self._mult.send, None), \
                    self._mult.result))

        self._mult.output[0] = 0  # Break the expected output.
        self.assertFalse(self._mult.verify(), "Verification did not fail: " \
                "got result {0}".format(self._mult.result))

if __name__ == "__main__":
    unittest.main()
