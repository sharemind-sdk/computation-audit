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

from . import block

class Summation(block.Block):

    """SMC summation protocol."""

    def __init__(self, input, output, context=None):
        """Instantiate a new summation protocol block with the given attributes.

        Args:
            input: A list of integers to be summed together. This is divided
                into equal-length slices and each individual slice is summed
                together. The number of slices is determined by the length of
                *output*.

            output: A list containing up to *len(input)* integers, where each
                integer is the expected sum of a slice of *input*. The length
                of *output* must be a divisor of the length of *input*.

            context: The context to use for simulation. A default is used if None.

        Raises:
            ValueError: If the length of *output* is not a divisor of the
                length of *input*.

        """
        super().__init__(input, output, context)

        if len(self.input) % len(self.output) != 0:
            raise ValueError("length of output must be a divisor of length of input")

    def _simulate(self):
        """Simulate the summation protocol with the input attributes."""
        n = len(self.output)
        slice_len = int(len(self.input) / n)

        # Take n slices from input, each slice_len long, and sum each slice to
        # an element of the result.
        return [sum(self.input[i * slice_len : (i + 1) * slice_len]) % self.context.mod
                for i in range(0, n)]
