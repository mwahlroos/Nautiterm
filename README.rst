Nautiterm - Open a terminal of your choice from Nautilus
========================================================

Nautiterm is an extension to the Nautilus file manager that opens a terminal
window of your choice at the location of the selected file.

The functionality is almost identical to other similar extensions, as well as
to the functionality provided by the Nautilus integration of Gnome Terminal,
available e.g. on Fedora as the ``gnome-terminal-nautilus`` package.

However, the current implementation provided by the Gnome Terminal Nautilus
integration always opens Gnome Terminal regardless of whether you would prefer
to use a different terminal emulator.

Nautiterm does the same but can be configured to open the terminal emulator
of your choice. The default is still to open Gnome Terminal.

Dependencies
------------

The extension requires the following:

- Python bindings for the Nautilus Extension Framework
- PYGObject, i.e. Python bindings for the GObject library
- PyYAML

On Fedora you can install the dependencies with the following command:

::

  sudo dnf install nautilus-python python3-yaml

On Ubuntu, the following command should install the dependencies:

::

  sudo apt install python-nautilus python-yaml

Installing
----------

There is no install routine yet. However, you can install the extension by
copying the file ``open_terminal.py`` into the Nautilus extensions folder:

::

  mkdir -p $HOME/.local/share/nautilus-python/extensions
  cp src/nautiterm/open_terminal.py $HOME/.local/share/nautilus-python/extensions

Then either log out and back in, or just shut down Nautilus:

::

  nautilus -q

The extension should be enabled the next time Nautilus is started.

You can uninstall the extension by removing the extension file:

::

  rm $HOME/.local/share/nautilus-python/extensions/open_terminal.py

Configuration
-------------

Out of the box with no configuration, Nautiterm opens a new Gnome Terminal
window. To have it open a different terminal emulator, such as `Terminator`_,
add a file named ``$HOME/.config/nautiterm.yml``, with the following contents:

.. _Terminator: https://launchpad.net/~gnome-terminator

::

  terminal: terminal_program

For example, to have Nautilus open Terminator instead of Gnome Terminal, the
configuration would usually be

::

  terminal: /usr/bin/terminator

In the above, ``$HOME`` refers to your home directory. On Linux, the correct
location for the configuration file would typically be
``/home/YOUR_USERNAME_HERE/.config``.

Caveats and TODO
----------------

There is no localization support yet.

Authors
-------

The code is based on `example code`_ written for the Python bindings for Nautilus
extensions.

.. _example code: https://gitlab.gnome.org/GNOME/nautilus-python/blob/master/examples/open-terminal.py

Modifications to the original code: © Mika Wahlroos (mika.wahlroos@iki.fi), 2019

Released under the GNU General Public License, version 2
