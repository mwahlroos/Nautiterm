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

"""Nautilus extension for opening a terminal window at the given/current location."""

import os
import os.path
import subprocess
import sys
import shutil
import yaml  # for loading configuration
import gi
from gi.repository import Nautilus, GObject

gi.require_version('Nautilus', '3.0')

PYTHON_MIN_MAJOR_VERSION = 3

if sys.version_info[0] < PYTHON_MIN_MAJOR_VERSION:
    raise RuntimeError('Nautiterm requires Python version 3.x or greater')

CONFIG_FILE_NAME = 'nautiterm.yml'
CONFIG_FILE_DIR = os.environ.get(
    'XDG_CONFIG_HOME', os.path.join(
        os.environ['HOME'], '.config'))
CONFIG_FILE_PATH = os.path.join(CONFIG_FILE_DIR, CONFIG_FILE_NAME)
DEFAULT_TERMINAL_EXEC = 'gnome-terminal'

print("Starting Nautiterm")


class Configuration:
    """Configuration of module"""

    def __init__(self):
        terminal = None

        try:
            with open(CONFIG_FILE_PATH, encoding="utf-8") as conffile:
                config = yaml.load(conffile, yaml.SafeLoader)
            terminal = config.get('terminal', None)
            self._display_name = config.get('display-name', True)
        except yaml.YAMLError:
            print(
                f'Nautiterm: invalid configuration file at {CONFIG_FILE_PATH}, ' +
                f'falling back to {DEFAULT_TERMINAL_EXEC}',
                file=sys.stderr)
        except IOError:
            # catch-all for permission errors and file not founds to be compatible
            # with Python 2 which doesn't have FileNotFoundError or
            # PermissionError
            pass

        if not terminal:
            terminal = DEFAULT_TERMINAL_EXEC

        self._terminal = terminal

    def get_terminal(self):
        """
        Returns the executable name of a terminal emulator to launch based on user
        configuration, or gnome-terminal if nothing else has been specified.
        """
        return self._terminal

    def is_display_name(self):
        """Returns flag that indicates is terminal name must be displayed into the context menu."""
        return self._display_name


class Terminal:
    """Terminal logic"""

    def __init__(self, configuration):
        self._configuration = configuration
        path = shutil.which(configuration.get_terminal())

        if not path:
            raise RuntimeError(
                f'Nautiterm: Unable to find configured terminal: {configuration.get_terminal()}')

        while os.path.islink(path):
            path = shutil.which(os.readlink(path))

        self._path = path
        self._name = os.path.basename(path)

    def open(self, file):
        """Launches the terminal"""
        open_path = file.get_location().get_path()

        if 'gnome-terminal' in self._name or 'terminator' in self._name:
            subprocess.run(
                [self._path, f'--working-directory={open_path}'], check=False)
        else:
            os.chdir(open_path)
            subprocess.run([self._path], check=False)

    def get_name(self):
        '''Returns terminal executable name without full path'''
        return self._name


class OpenTerminalExtension(Nautilus.MenuProvider, GObject.GObject):
    """Class implements Mautiterm module """

    def __init__(self):
        self._configuration = Configuration()
        self._terminal = Terminal(self._configuration)

    def _menu_activate_cb(self, _, file):
        self._terminal.open(file)

    def _menu_background_activate_cb(self, _, file):
        self._terminal.open(file)

    def get_file_items(self, _, files):  # pylint: disable=arguments-differ
        '''Adds menu item for files and directories'''

        if len(files) != 1:
            return None

        file = files[0]
        if not file.is_directory() or file.get_uri_scheme() != 'file':
            return None

        label = 'Open Terminal'
        if self._configuration.is_display_name():
            label += f' ({self._terminal.get_name()})'

        item = Nautilus.MenuItem(
            name='NautilusPython::openterminal_file_item',
            label=label,
            tip=f'Open Terminal In {file.get_name()}')
        item.connect('activate', self._menu_activate_cb, file)
        return (item,)

    def get_background_items(self, _, file): # pylint: disable=arguments-differ
        '''Adds menu item for current directory'''

        label = 'Open Terminal'
        if self._configuration.is_display_name():
            label += f' ({self._terminal.get_name()})'

        item = Nautilus.MenuItem(
            name='NautilusPython::openterminal_file_item2',
            label=label,
            tip=f'Open Terminal In {file.get_name()}')
        item.connect('activate', self._menu_background_activate_cb, file)

        return (item,)
