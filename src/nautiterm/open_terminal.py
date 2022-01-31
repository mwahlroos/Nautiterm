# Nautilus extension for opening a terminal window at the given/current location.
#
# Based on example code from the Nautilus Python project, retrieved from
# https://gitlab.gnome.org/GNOME/nautilus-python/blob/master/examples/open-terminal.py
#
# The original example is contributed by Martin Enlund
#
# Modifications made by Mika Wahlroos (mika.wahlroos@iki.fi):
# - Read the name/path of the terminal executable from a config file if present
# - Use the file URI/path functions from PyGObject to get the path to the
#   current location based on the file URI rather than just assuming a file://
#   URI

from __future__ import print_function

import os
import os.path
import subprocess
import sys
import yaml  # for loading configuration
import gi

gi.require_version('Nautilus', '3.0')
from gi.repository import Nautilus, GObject, Gio

CONFIG_FILE_NAME = 'nautiterm.yml'
CONFIG_FILE_DIR = os.environ.get('XDG_CONFIG_HOME',
                                 os.path.join(os.environ['HOME'], '.config'))
CONFIG_FILE_PATH = os.path.join(CONFIG_FILE_DIR, CONFIG_FILE_NAME)
DEFAULT_TERMINAL_EXEC = 'gnome-terminal'

print("Starting Nautiterm")


class OpenTerminalExtension(Nautilus.MenuProvider, GObject.GObject):

    def __init__(self):
        pass

    def _open_terminal(self, file):
        gvfs = Gio.Vfs.get_default()
        open_path = gvfs.get_file_for_uri(file.get_uri()).get_path()

        exc = self._get_terminal_exec()
        if 'gnome-terminal' in exc or 'terminator' in exc:
            subprocess.Popen([self._get_terminal_exec(), '--working-directory={p}'.format(p=open_path)])
        else:
            os.chdir(open_path)
            subprocess.Popen([exc])

    def _get_terminal_exec(self):
        """
        Returns the executable name of a terminal emulator to launch based on user
        configuration, or gnome-terminal if nothing else has been specified.
        """

        terminal = None

        try:
            with open(CONFIG_FILE_PATH) as conffile:
                config = yaml.load(conffile, yaml.SafeLoader)
            terminal = config.get('terminal', None)
        except yaml.YAMLError:
            print("Nautiterm: invalid configuration file at {path}, falling back" +
                  " to {d}".format(path=CONFIG_FILE_PATH, d=DEFAULT_TERMINAL_EXEC),
                  file=sys.stderr)
        except IOError as ioe:
            # catch-all for permission errors and file not founds to be compatible
            # with Python 2 which doesn't have FileNotFoundError or PermissionError
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
                                 label='Open Terminal (%s)' % self._get_terminal_exec(),
                                 tip='Open Terminal In %s' % file.get_name())
        item.connect('activate', self.menu_activate_cb, file)
        return item,

    def get_background_items(self, window, file):
        item = Nautilus.MenuItem(name='NautilusPython::openterminal_file_item2',
                                 label='Open Terminal (%s)' % self._get_terminal_exec(),
                                 tip='Open Terminal In %s' % file.get_name())
        item.connect('activate', self.menu_background_activate_cb, file)
        return item,
