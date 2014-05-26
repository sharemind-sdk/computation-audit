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

from ..core import protocol as smprotocol
from . import _util as util

from kivy.uix.treeview import TreeViewLabel

import collections

_Variable = collections.namedtuple("_Variable", "name value")

def _format_variable(name, value):
    return _Variable(util.format_value(name, util.int_to_color(sum(value))),
                     util.format_values(value))

def _sub(name, sub):
    # Hard-code the subscript size to 9 instead of .5 * font_size. A better
    # solution would be to force it to .75 * font_size.
    return "{0}[sub][size=9]{1}[/size][/sub]".format(name, sub)

def _format_multiplication(protocol):
    return "{A.name} := {A.value}\n" \
           "{B.name} := {B.value}\n" \
           "{RPA.name} <- R ({RPA.value})\n" \
           "{RPB.name} <- R ({RPB.value})\n" \
           "Send {RPA.name} and {RPB.name} to the previous party.\n" \
           "{ASN.name} := {A.name} - {RPA.name} = {ASN.value}\n" \
           "{BSN.name} := {B.name} - {RPB.name} = {BSN.value}\n" \
           "{RSN.name} <- R ({RSN.value})\n" \
           "Send {ASN.name}, {BSN.name}, and {RSN.name} to the next party.\n" \
           "Receive {RA.name} and {RB.name} from the next party, where\n" \
           "    {RA.name} = {RA.value},\n" \
           "    {RB.name} = {RB.value}.\n" \
           "Receive {AP.name}, {BP.name}, and {RP.name} from the previous party, where\n" \
           "    {AP.name} = {AP.value},\n" \
           "    {BP.name} = {BP.value},\n" \
           "    {RP.name} = {RP.value}.\n" \
           "{Apr.name} := {A.name} + {RA.name} = {Apr.value} (reshared {A.name})\n" \
           "{Bpr.name} := {B.name} + {RB.name} = {Bpr.value} (reshared {B.name})\n" \
           "{APpr.name} := {AP.name} + {RPA.value} = {APpr.value} (reshared {AP.name})\n" \
           "{BPpr.name} := {BP.name} + {RPB.value} = {BPpr.value} (reshared {BP.name})\n" \
           "return {Apr.name}*{Bpr.name} + {Apr.name}*{BPpr.name} + {Bpr.name}*{APpr.name} " \
           "+ {RSN.name} - {RP.name} = {res}".format(
               A    = _format_variable("A", protocol.input[0]),
               B    = _format_variable("B", protocol.input[1]),
               RPA  = _format_variable(_sub("R", "prevA"), protocol.result.send["prev"][0]),
               RPB  = _format_variable(_sub("R", "prevB"), protocol.result.send["prev"][1]),
               ASN  = _format_variable(_sub("A", "sendNext"), protocol.result.send["next"][0]),
               BSN  = _format_variable(_sub("B", "sendNext"), protocol.result.send["next"][1]),
               RSN  = _format_variable(_sub("R", "sendNext"), protocol.result.send["next"][2]),
               RA   = _format_variable(_sub("R", "A"), protocol.recv["next"][0]),
               RB   = _format_variable(_sub("R", "B"), protocol.recv["next"][1]),
               AP   = _format_variable(_sub("A", "prev"), protocol.recv["prev"][0]),
               BP   = _format_variable(_sub("B", "prev"), protocol.recv["prev"][1]),
               RP   = _format_variable(_sub("R", "prev"), protocol.recv["prev"][2]),
               Apr  = _format_variable("A'", protocol.result.simulation.vec_a),
               Bpr  = _format_variable("B'", protocol.result.simulation.vec_b),
               APpr = _format_variable(_sub("A'", "prev"), protocol.result.simulation.vec_ap),
               BPpr = _format_variable(_sub("B'", "prev"), protocol.result.simulation.vec_bp),
               res  = util.format_values(protocol.result.output))

def _format_declassification(protocol):
    received = list(protocol.recv["computing"])
    for i in range(0, len(received)):
        received[i] = _format_variable(_sub("V", str(i + 1)), received[i])

    return "{V.name} := {V.value}\n" \
           "{R.name} <- R ({R.value})\n" \
           "Send {R.name} to the next party.\n" \
           "Receive {RP.name} from the previous party, where\n" \
           "    {RP.name} = {RP.value}.\n" \
           "{Vp.name} := {V.name} + {RP.name} - {R.name} = {Vp.value} (reshared {V.name})\n" \
           "Send {Vp.name} to all remote parties.\n" \
           "Receive shares V[sub]*[/sub] from all remote computing parties, where\n" \
           "    {received_where}.\n" \
           "return sum({Vp.name}, {received_sum}) = {res}".format(
               V  = _format_variable("V", protocol.input),
               R  = _format_variable("R", protocol.result.send["next"]),
               RP = _format_variable(_sub("R", "prev"), protocol.recv["prev"]),
               Vp = _format_variable("V'", protocol.result.send["remote"]),
               received_where = ",\n    ".join(map("{0.name} = {0.value}".format, received)),
               received_sum   = ", ".join(map(lambda v: v.name, received)),
               res = util.format_values(protocol.result.output))

# A dict from protocol type to a function that formats its body.
_protocol_bodies = {
        smprotocol.Multiplication:   _format_multiplication,
        smprotocol.Declassification: _format_declassification,
    }

def _format_body(protocol):
    return _protocol_bodies[type(protocol)](protocol)

class ProtocolBody(TreeViewLabel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = _format_body(kwargs["protocol"])
