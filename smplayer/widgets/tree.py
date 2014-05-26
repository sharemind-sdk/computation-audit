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

from ..core import smplayer
from ..core import protocol as smprotocol
from .header import ProtocolHeader
from .body import ProtocolBody
from . import _util as util

from kivy.uix.treeview import TreeView, TreeViewLabel

def _color_hashes(h):
    def color(v):
        if v:
            return util.format_value(v, util.int_to_color(sum(map(ord, v))))
        return v

    return h._replace(send_prev=color(h.send_prev), send_next=color(h.send_next),
            send_remote=color(h.send_remote), recv_prev=color(h.recv_prev),
            recv_next=color(h.recv_next), recv_computing=list(map(color, h.recv_computing)))

def _format_hashes(hashes):
    hashes = _color_hashes(hashes) if hashes \
            else smplayer.MessageHash(None, None, None, None, None, [])
    return "Messages sent to the previous party: {h.send_prev}\n" \
           "Messages sent to the next party: {h.send_next}\n" \
           "Messages sent to all remote parties: {h.send_remote}\n" \
           "Messages received from the previous party: {h.recv_prev}\n" \
           "Messages received from the next party: {h.recv_next}\n" \
           "Messages received from remote computing parties:\n" \
           "    {computing}".format(h=hashes, computing="\n    ".join(hashes.recv_computing))

class ProtocolTree(TreeView):

    """A TreeView of the audited protocols."""

    def __init__(self, **kwargs):
        player = kwargs["player"]
        root_options = kwargs["root_options"]
        root_options["text"] = "{0} {1}".format(util.format_ok(player.verify()), root_options["text"])

        super().__init__(**kwargs)
        self.bind(minimum_height=self.setter("height"))

        self.add_node(TreeViewLabel(text=_format_hashes(player.hash())))
        for protocol in player.protocols:
            header = ProtocolHeader(protocol=protocol)
            self.add_node(header)
            if isinstance(protocol, smprotocol.Protocol):
                self.add_node(ProtocolBody(protocol=protocol), header)
