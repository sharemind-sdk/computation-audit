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
import os

import smplayer.core._parser as parser
import smplayer.core.protocol as protocol

class TestParser(unittest.TestCase):

    def test_parse_log(self):
        basedir = os.path.dirname(__file__)
        if basedir:
            basedir += '/'
        protocols = parser.parse_log(basedir + "data/audit.log")

        self.assertIsInstance(protocols[0], protocol.Multiplication)
        self.assertTrue(protocols[0].verify(), "Parsed multiplication protocol did not verify")

        self.assertIsInstance(protocols[1], protocol.Subtraction)
        self.assertTrue(protocols[1].verify(), "Parsed subtraction protocol did not verify")

        self.assertIsInstance(protocols[2], protocol.Declassification)
        self.assertTrue(protocols[2].verify(), "Parsed declassification protocol did not verify")

        self.assertIsInstance(protocols[9], protocol.Summation)
        self.assertTrue(protocols[9].verify(), "Parsed summation protocol did not verify")

        self.assertIsInstance(protocols[22], protocol.Addition)
        self.assertTrue(protocols[22].verify(), "Parsed addition protocol did not verify")

if __name__ == "__main__":
    unittest.main()
