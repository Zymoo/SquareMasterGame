import gi

from src.common.Commons import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

from src.common.AppModel import AppModel


class AppScreen(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Mistrz szachownicy GTK")

        self.engine = AppModel()
        self.gameFlag = False
        self.timeCounter = TIME_LIMIT

        self.set_default_size(800, 900)
        self.set_size_request(800, 900)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(self.box)
        self._OverviewSetUp()
        self._boardSetUp()
        self._progressBarSetUp()
        self._menuSetUp()
        self._statsSetUp()
        self._makeItPretty()

    def _makeItPretty(self):
        css = b"""
        button {
            border-style: solid;
            border-color: gray;
            border-width: 1px;
        }
        
        button:disabled * {
            color:gray
        }
        
        #overview {
            color: black;
            border: 2px solid gray;
            border-radius: 10px;
            padding: 6px;
            margin: 8px;
            background: cornsilk;
            font-family: Arial, Helvetica;
            font-size: 15px;
        }
        
        #stats {
            color: black;
            border: 2px solid gray;
            padding: 0px;
            border-radius: 10px;
            margin: 4px;
            background: cornsilk;
            min-height: 40px;
        }
        
        #menu {
            color: black;
            margin: 4px;
            padding: 0px;
            border-style: solid;
            border-color: gray;
            border-width: 2px;
            border-radius: 10px;
            background: cornsilk;
            min-height: 40px;
        }
        
        progress {
            min-height: 20px;
        }
        
        progressbar, trough {
            min-height: 20px;
            margin: 2px;
            padding: 2px;
        }
        
        #whitesquare {
            background: linen;
        }
        
        #blacksquare {
            background: sienna;
        }
        
        #redsquare {
            background: red;
        }
        
        #greensquare {
            background: green;
        }
        
        #boxframe {
            padding: 10px;
        }
        
        """

        self.box.set_name("boxframe")

        self.overview.set_name("overview")

        self.scoreStatic.set_name("stats")
        self.score.set_name("stats")
        self.coordStatic.set_name("stats")
        self.coord.set_name("stats")
        self.startButton.set_name("menu")
        self.stopButton.set_name("menu")

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider,
                                        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def _progressBarSetUp(self):
        self.progressbar = Gtk.ProgressBar()
        self.box.pack_start(self.progressbar, False, False, 0)

    def _OverviewSetUp(self):
        self.overviewBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.overview = Gtk.Label(OVERVIEW_TEXT)

        self.overview.set_line_wrap(True)
        self.overviewBox.pack_start(self.overview, True, True, 0)
        self.box.pack_start(self.overviewBox, True, True, 0)

    def _statsSetUp(self):
        self.stats = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True)

        self.scoreStatic = Gtk.Label("Aktualny wynik:")
        self.score = Gtk.Label("0")
        self.coordStatic = Gtk.Label("Znajdź:")
        self.coord = Gtk.Label("")

        self.stats.add(self.scoreStatic)
        self.stats.add(self.score)
        self.stats.add(self.coordStatic)
        self.stats.add(self.coord)
        self.box.pack_start(self.stats, False, False, 0)

    def _menuSetUp(self):
        self.menu = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True)

        self.startButton = Gtk.Button("Start")
        self.startButton.connect("clicked", self._onStartClick)
        self.menu.add(self.startButton)

        self.stopButton = Gtk.Button("Stop")
        self.stopButton.connect("clicked", self._onStopClick)
        self.stopButton.set_sensitive(False)
        self.menu.add(self.stopButton)

        self.box.pack_start(self.menu, False, False, 0)

    def _boardSetUp(self):
        self.gameBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.grid = Gtk.Grid()
        self.grid.set_size_request(560, 560)
        self.gameBox.pack_start(self.grid, False, False, 0)
        self.box.pack_start(self.gameBox, False, False, 0)

        for i in range(8 * 8):
            newButton = Gtk.Button()
            newButton.set_hexpand(True)
            newButton.set_vexpand(True)
            newButton.connect("pressed", self._onSquareClick)
            newButton.connect("released", self._onSquareRelease)
            x = getX(i)
            y = getY(i)
            if (x + y) % 2 == 0:
                newButton.set_name("whitesquare")
            else:
                newButton.set_name("blacksquare")
            self.grid.attach(newButton, x, y, 1, 1)

    def _onStartClick(self, btn):
        if self.gameFlag:
            return
        self.startButton.set_sensitive(False)
        self.stopButton.set_sensitive(True)
        self.gameFlag = True
        self.timeout_id = GLib.timeout_add(TIME_INTERVAL, self._onClockChanged)
        self.timeCounter = TIME_LIMIT

        self.engine.counterReset()
        self.engine.getNextPosition()
        self.coord.set_label(self.engine.getCurrentNotation())
        self.score.set_label("0")

    def _onStopClick(self, btn):
        if not self.gameFlag:
            return
        self.stopButton.set_sensitive(False)
        self.gameFlag = False

    def _onClockChanged(self):
        if (self.timeCounter == 0) or (self.gameFlag is False):
            self.startButton.set_sensitive(True)
            self.stopButton.set_sensitive(False)
            self.gameFlag = False
            return False
        self.timeCounter -= 1
        self.progressbar.set_fraction(self.timeCounter / TIME_LIMIT)
        return True

    def _onSquareClick(self, btn):
        if not self.gameFlag:
            return
        x = self.grid.child_get_property(btn, "top-attach")
        y = self.grid.child_get_property(btn, "left-attach")

        if self.engine.getCurrentPosition() == (x, y):
            btn.set_name("greensquare")
            self.engine.counterAdd()
            self.engine.getNextPosition()
            self.coord.set_label(self.engine.getCurrentNotation())
            self.score.set_label(str(self.engine.getCounter()))
            return
        btn.set_name("redsquare")

    def _onSquareRelease(self, btn):
        x = self.grid.child_get_property(btn, "top-attach")
        y = self.grid.child_get_property(btn, "left-attach")

        if (x + y) % 2 == 0:
            btn.set_name("whitesquare")
        else:
            btn.set_name("blacksquare")
