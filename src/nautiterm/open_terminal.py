# Nautilus extension for opening a terminal window at the current location.
#
# Based on example code from the Nautilus Python project, retrieved from
# https://gitlab.gnome.org/GNOME/nautilus-python/blob/master/examples/open-terminal.py
#
# The original example is contributed by Martin Enlund

from __future__ import print_function

import os, sys
import yaml  # for loading configuration

# A way to get unquote working with python 2 and 3
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

import gi

gi.require_version('GConf', '2.0')
gi.require_version('Nautilus', '3.0')
from gi.repository import Nautilus, GObject, GLib, GConf

CONFIG_FILE_NAME = '.nautiterm.conf'
DEFAULT_TERMINAL_EXEC = 'gnome-terminal'


class OpenTerminalExtension(Nautilus.MenuProvider, GObject.GObject):
    def __init__(self):
        self.client = GConf.Client.get_default()

    def _open_terminal(self, file):
        filename = unquote(file.get_uri())[7:]
        # filename = unquote(GLib.filename_from_uri(file.get_uri()))

        os.chdir(filename)
        os.system(self._get_terminal_exec())

    def _get_terminal_exec(self):
        """
        Returns the executable name of a terminal emulator to launch based on user
        configuration, or gnome-terminal if nothing else has been specified.
        """
        config_path = os.environ['HOME'] + os.sep + CONFIG_FILE_NAME

        terminal = None

        try:
            with open(config_path) as conffile:
                config = yaml.load(conffile, yaml.SafeLoader)
            terminal = config.get('terminal', None)
        except yaml.YAMLError:
            print("NautiTerm: invalid configuration file at {path}, falling back" +
                  " to {d}".format(path=config_path, d=DEFAULT_TERMINAL_EXEC),
                  file=sys.stderr)
        except PermissionError:
            print("NautiTerm: no permission to read configuration file at " +
                  "{path}, falling back to {d}".format(path=config_path,
                                                       d=DEFAULT_TERMINAL_EXEC),
                  file=sys.stderr)
        except FileNotFoundError:
            pass

        if not terminal:
            terminal = DEFAULT_TERMINAL_EXEC

        return terminal

    def menu_activate_cb(self, menu, file):
        self._open_terminal(file)

    def menu_background_activate_cb(self, menu, file):
        self._open_terminal(file)

    def get_file_items(self, window, files):
        if len(files) != 1:
            return

        file = files[0]
        if not file.is_directory() or file.get_uri_scheme() != 'file':
            return

        item = Nautilus.MenuItem(name='NautilusPython::openterminal_file_item',
                                 label='Open Terminal',
                                 tip='Open Terminal In %s' % file.get_name())
        item.connect('activate', self.menu_activate_cb, file)
        return item,

    def get_background_items(self, window, file):
        item = Nautilus.MenuItem(name='NautilusPython::openterminal_file_item2',
                                 label='Open Terminal',
                                 tip='Open Terminal In %s' % file.get_name())
        item.connect('activate', self.menu_background_activate_cb, file)
        return item,
