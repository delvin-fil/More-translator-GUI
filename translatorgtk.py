#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings("ignore")
import os
import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from langdetect import detect
import translators as ts
#from textblob import TextBlob

CURRDIR = os.path.dirname(os.path.abspath(__file__))
ICON = os.path.join(CURRDIR, 'icon.png')

err = "Buffer empty!"

def clip():
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
    clip = clipboard.wait_for_text()
    if not clip.strip() or not clip:
        clip = err
    #if clip.isalnum():
    else:
        clip = clip
    return clip

indetect = detect(clip())

def detec():
    dettext = detect(clip())
    if dettext == 'ru':
        langout = 'en'
    else:
        langout = 'ru'
    return langout

def translate():
    output = []
    #blob = TextBlob(clip())
    #numb = len((blob.sentences))
    output = ts.google(clip(), to_language=detec(), if_use_cn_host=True)
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
        self.set_title(f"Translate google {indetect}-{detec()}")

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
