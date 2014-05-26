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

from . import core, widgets

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

import os
import types

class LoadDialog(Popup):

    """A popup dialog for loading files."""

    load = ObjectProperty(None, baseclass=types.MethodType)
    """The callback to invoke when a file is selected for loading."""

class SMPlayerWindow(BoxLayout):

    """The main window of the application."""

    view = ObjectProperty(None, baseclass=ScrollView)
    """Reference to the ScrollView containing the ProtocolTree."""

    player = ObjectProperty(core.SMPlayer(), baseclass=core.SMPlayer)
    """Reference to a Sharemind Player instance."""

    def show_load(self):
        """Show a popup dialog to choose the file to load."""
        self._load_dialog = LoadDialog(load=self.load)
        self._load_dialog.open()

    def load(self, path, filename):
        """Load an audit log from the given location and display it's ProtocolTree."""
        if not filename:
            return
        full_path = os.path.join(path, filename[0])
        try:
            self.player.open(full_path)
        except core.LogError as e:
            Popup(title="Error loading " + filename[0], content=Label(text=str(e)),
                    size_hint=(None, None), size=(600, 200)).open()
        else:
            self.view.clear_widgets()
            self.view.add_widget(widgets.ProtocolTree(player=self.player,
                    root_options={ "text": full_path }))
            self._load_dialog.dismiss()

class SMPlayerApp(App):

    """The main kivy application."""

    def build(self):
        self.title = "Sharemind Player"
        return SMPlayerWindow()
