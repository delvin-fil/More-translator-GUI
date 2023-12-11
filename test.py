import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

try:
    display = Gdk.Display.get_default()
    clipboard = Gtk.Clipboard.get_for_display(display, Gdk.SELECTION_CLIPBOARD)
except AttributeError:
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

print(clipboard)