import gi

from src.AppScreen import AppScreen

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

if __name__ == '__main__':
    window = AppScreen()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
