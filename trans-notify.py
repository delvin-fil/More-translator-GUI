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
from pydbus import SessionBus
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, Pango, Notify, GLib
from langdetect import detect
import translators as ts
import translators.server as tss


pver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
engine = 'bing'
#engine = 'google'


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
    
    elif engine == 'bing' :
        output = tss.bing(clip(), to_language=definition(), professional_field='general')

    else:
        output = tss.google(clip(), to_language=definition(), professional_field='general', proxies=proxy)

    return output

def close_notification_cb(notification):
    notification.close()
    loop.quit() 
    return False


bus = SessionBus()
Notify.init("Translator")

notification = Notify.Notification.new(
    f"Translate {engine}",
    f"<span font='16'>{translate()}</span>",
    ICON
)
timeout = 5
notification.show()
GLib.timeout_add_seconds(timeout, close_notification_cb, notification)
loop = GLib.MainLoop()
loop.run()
Notify.uninit()