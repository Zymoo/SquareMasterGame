import gi

from AppScreenGtk import AppScreenG

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

if __name__ == '__main__':
    window = AppScreenG()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
