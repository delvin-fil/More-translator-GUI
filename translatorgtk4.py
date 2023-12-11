#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
'''
https://github.com/uliontse/translators
'''
import warnings
warnings.filterwarnings("ignore")
import os
import re
import gi
gi.require_version('Gdk', '4.0')
gi.require_version('Gtk', '4.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from langdetect import detect
import translators as ts
import translators.server as tss

engine = 'bing'
#engine = 'google'
#engine = 'Deepl'

CURDIR = os.path.dirname(os.path.abspath(__file__))
ICON = os.path.join(CURDIR, f'{engine}.png')

err = "Buffer empty!!!"
proxy = {'address': '127.0.0.1', 'port': 9050}

def clip():
    clipboard = Gdk.Display.get_default().get_clipboard()
    future = clipboard.read_text_async()
    future.on_result(print_clipboard_text, clipboard)
    print(future.get())
    if not clipboard:
        clip = err
    else:
        clip = future.get()
    return clip
print(clip())
indetect = detect(clip())

def definition():
	if indetect == 'ru':
		langout = 'en'
	else:
		langout = 'ru'
	return langout

def translate():
    output = []
    
    if engine == 'bing' :
        output = tss.bing(clip(), to_language=definition(), professional_field='general')

    else:
        output = tss.google(clip(), to_language=definition(), professional_field='general')

    return output

class TextViewWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=f"Translate {engine} {indetect}-{definition()}")
        self.set_default_size(1000, 350)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.box = Gtk.Box(Gtk.Orientation.VERTICAL, spacing=0) 
        self.set_child(self.box) 
        self.create_textview()
        self.create_toolbar()
        self.key_Esc = Gdk.keyval_from_name("Escape")

        self.connect("key-pressed-event", self._key)
  
    def create_toolbar(self):
        toolbar = Gtk.Box(Gtk.Orientation.HORIZONTAL, spacing=0) 
        new_button = Gtk.Button.new_icon_from_name("window-close-symbolic")
        new_button.connect("clicked", self.on_button_clicked, self.tag_bold)
        toolbar.append(new_button)
        self.box.append(toolbar)
        
    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        self.grid.attach(scrolledwindow, 0, 0, 2, 1)
        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(f"{translate()}")
        scrolledwindow.set_child(self.textview)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
        self.textview.set_font(Pango.FontDescription('Menlo Regular 24'))
 
    def _key(self, widg, event):
        if event.keyval == self.key_Esc:
            Gtk.main_quit()

    def on_button_clicked(self, widget, tag):
        Gtk.main_quit()

win = TextViewWindow()
win.connect("destroy", Gtk.main_quit)
win.show()
Gtk.main()
