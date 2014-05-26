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

class TestDeclassificationProtocol(unittest.TestCase):

    def setUp(self):
        input = [965506304, 965506304]
        output = [0, 0]
        send = { "next": [3924503522, 3924503522],
                 "remote": [2905908703, 2905908703] }
        recv = { "prev": [1569938625, 1569938625],
                 "computing": ([3972596883, 3972596883], [1711429006, 1711429006]) }

        self._declass = protocol.Declassification( \
                input, output, send, recv)

    def test_verify(self):
        self.assertTrue(self._declass.verify(), "Verification failed: " \
                "expected {0}, but got {1}".format( \
                    protocol.ProtocolResult(self._declass.output, self._declass.send, None), \
                    self._declass.result))

        self._declass.output[0] = 1  # Break the expected output.
        self.assertFalse(self._declass.verify(), "Verification did not fail: " \
                "got result {0}".format(self._declass.result))

if __name__ == "__main__":
    unittest.main()
