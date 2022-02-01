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
# - Assume Python 3.x

import os
import os.path
import subprocess
import sys
import yaml  # for loading configuration
import gi
import shutil

gi.require_version('Nautilus', '3.0')
from gi.repository import Nautilus, GObject

PYTHON_MIN_MAJOR_VERSION = 3

if sys.version_info[0] < PYTHON_MIN_MAJOR_VERSION:
    raise RuntimeError('Nautiterm requires Python version 3.x or greater')

CONFIG_FILE_NAME = 'nautiterm.yml'
CONFIG_FILE_DIR = os.environ.get('XDG_CONFIG_HOME',
                                 os.path.join(os.environ['HOME'], '.config'))
CONFIG_FILE_PATH = os.path.join(CONFIG_FILE_DIR, CONFIG_FILE_NAME)
DEFAULT_TERMINAL_EXEC = 'gnome-terminal'

print("Starting Nautiterm")

class Configuration:

    def __init__(self):
        terminal = None

        try:
            with open(CONFIG_FILE_PATH) as conffile:
                config = yaml.load(conffile, yaml.SafeLoader)
            terminal = config.get('terminal', None)
            self.display_name = config.get('display-name', True)
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

        """
        Contains the executable name of a terminal emulator to launch based on user
        configuration, or gnome-terminal if nothing else has been specified.
        """
        self.terminal = terminal

class Terminal:

    def __init__(self, configuration):
        self.configuration = configuration
        path = shutil.which(configuration.terminal);

        if not path:
            raise RuntimeError('Nautiterm: Unable to find configured terminal: %s' % configuration.terminal)

        while os.path.islink(path):
            path = shutil.which(os.readlink(path))

        self.path = path
        self.name = os.path.basename(path)

    def open(self, file):
        open_path = file.get_location().get_path()

        if 'gnome-terminal' in self.name or 'terminator' in self.name:
            subprocess.Popen([self.path, '--working-directory={p}'.format(p=open_path)])
        else:
            os.chdir(open_path)
            subprocess.Popen([self.path])


class OpenTerminalExtension(Nautilus.MenuProvider, GObject.GObject):

    def __init__(self):
        self.configuration = Configuration()
        self.terminal = Terminal(self.configuration)

    def menu_activate_cb(self, menu, file):
        self.terminal.open(file)

    def menu_background_activate_cb(self, menu, file):
        self.terminal.open(file)

    def get_file_items(self, window, files):
        if len(files) != 1:
            return

        file = files[0]
        if not file.is_directory() or file.get_uri_scheme() != 'file':
            return

        label = 'Open Terminal'
        if self.configuration.display_name:
            label += ' (%s)' % self.terminal.name

        item = Nautilus.MenuItem(name='NautilusPython::openterminal_file_item',
                                 label=label,
                                 tip='Open Terminal In %s' % file.get_name())
        item.connect('activate', self.menu_activate_cb, file)
        return item,

    def get_background_items(self, window, file):
        label = 'Open Terminal'
        if self.configuration.display_name:
            label += ' (%s)' % self.terminal.name

        item = Nautilus.MenuItem(name='NautilusPython::openterminal_file_item2',
                                 label=label,
                                 tip='Open Terminal In %s' % file.get_name())
        item.connect('activate', self.menu_background_activate_cb, file)
        return item,
