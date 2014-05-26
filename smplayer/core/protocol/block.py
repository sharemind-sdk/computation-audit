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

from . import context as ctx

class Block(object):

    """A block of code with input and output values.

    This is an abstract base class and the actual contained code is specified
    by inheriting classes.

    Attributes:
        input: The given input to the code block.
        output: The expected output of the code block.
        context: Necessary context for protocol simulation.

    """

    def __init__(self, input, output, context=None):
        """Instantiate a new code block with *input*, *output*, and optionally *context*.

        If no context is given, the default context is used.

        """
        self._cached = None
        self.input = input
        self.output = output
        self.context = context if context else ctx.default_context

    @property
    def result(self):
        """The result of simulating this code block with *input*.

        The block is simulated and the result stored the first time this is
        read. Use clear_cache() to clear the cache and force resimulation
        on the next read.

        """
        if self._cached == None:
            self._cached = self._simulate()
        return self._cached

    def clear_cache(self):
        """Clear the cached simulation result and force re-simulation."""
        self._cached = None

    def _simulate(self):
        """Execute the code block with *input* and return the result."""
        raise NotImplementedError

    def verify(self):
        """Verify the attributes.

        Check if this code block with *input* returns a result equal to *output*.

        Returns:
            True if the calculated result is equal to the expected output.

        """
        return self.result == self.output
