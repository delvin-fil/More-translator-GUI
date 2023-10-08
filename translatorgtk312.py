#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
'''
https://github.com/uliontse/translators
'''
import warnings
warnings.filterwarnings("ignore")
import os
import re
import sys
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, Pango
#from gi.repository import 
#from gi.repository import 
from langdetect import detect
import translators as ts
import translators.server as tss


pver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
engine = 'bing'
engine = 'google'
#engine = 'Deepl'

CURDIR = os.path.dirname(os.path.abspath(__file__))
ICON = os.path.join(CURDIR, f'{engine}.png')

err = "Buffer empty!!!"
proxy = {'address': '127.0.0.1', 'port': 9050}

def clip():
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
    clip = clipboard.wait_for_text()
    if not clip.strip() or not clip:
        clip = err
    else:
        clip = str(clip)
    return clip
txt = clip()
txt = re.sub(r'“|”|»|«', '\"', txt)
#
print(txt)
indetect = detect(txt)

def definition():
    if indetect == 'ru':
        langout = 'en'
    else:
        langout = 'ru'
    return langout

def translate():
    output = []
    
    if engine == 'Deepl' :
        output = tss.deepl(clip(), from_language=indetect, to_language=definition(), if_use_cn_host=False, proxies=proxy)
    elif engine == 'bing' :
        output = tss.bing(clip(), to_language=definition(), professional_field='general')

    else:
        output = tss.google(clip(), to_language=definition(), professional_field='general')

    return output

class TextViewWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(1000, 350)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.create_textview()
        self.create_toolbar()
        self.init_ui()
        self.key_Esc = Gdk.keyval_from_name("Escape")
        self.connect("key-press-event", self._key)

    def init_ui(self):
        self.set_title(f"Translate {engine} {indetect}-{definition()}, Python ver: {pver}")

    def create_toolbar(self):
        toolbar = Gtk.Toolbar()
        self.grid.attach(toolbar, 1, 1, 1, 1)
        new_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_CLOSE)
        new_button.set_is_important(True)
        toolbar.insert(new_button, 0)
        new_button.connect("clicked", self.on_button_clicked, self.tag_bold)
        new_button.show()

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 0, 2, 1)
        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(f"{translate()}")
        scrolledwindow.add(self.textview)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.tag_bold = self.textbuffer.create_tag("bold",
                                                   weight=Pango.Weight.BOLD)
        self.textview.modify_font(Pango.FontDescription('Menlo Regular 24'))

    def _key(self, widg, event):
        if event.keyval == self.key_Esc:
            Gtk.main_quit()

    def on_button_clicked(self, widget, tag):
        Gtk.main_quit()

win = TextViewWindow()
win.connect("destroy", Gtk.main_quit)
win.set_icon_from_file(ICON)
win.show_all()
Gtk.main()
