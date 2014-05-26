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

class Subtraction(block.Block):

    """SMC subtraction protocol."""

    def __init__(self, input, output, context=None):
        """Instantiate a new subtraction protocol block with the given attributes.

        Args:
            input: A pair containing equal-length lists of integers, where the
                second list will be subtracted from the first one elementwise.

            output: The expected result of subtracting the second input list
                from the first. Must be the same length as the input lists.

            context: The context to use for simulation. A default is used if None.

        Raises:
            ValueError: If any ony of the lists are of invalid length.

        """
        super().__init__(input, output, context)

        if len(self.input) != 2:
            raise ValueError("input must contain two elements")
        n = len(self.input[0])

        if len(self.input[1]) != n:
            raise ValueError("The lists in input must have equal length")

        if len(self.output) != n:
            raise ValueError("The output list must be the same length as the input lists")

    def _simulate(self):
        """Simulate the subtraction protocol with the input attributes."""
        return [(a - b) % self.context.mod for (a, b) in zip(self.input[0], self.input[1])]
