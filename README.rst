Nautiterm - Open a terminal of your choice from Nautilus
========================================================

Nautiterm is an extension to the Nautilus file manager that opens a terminal
window of your choice at the location of the selected file.

The functionality is almost identical to other similar extensions, as well as
to the functionality provided by the Nautilus integration of Gnome Terminal,
available e.g. on Fedora as the gnome-terminal-nautilus package.

However, the current implementation provided by the Gnome Terminal Nautilus
integration always opens Gnome Terminal regardless of whether you would prefer
to use a different terminal emulator.

Nautiterm does the same but can be configured to open the terminal emulator
of your choice. The default is still to open Gnome Terminal.

Installing
----------

TODO

Configuration
-------------

Out of the box with no configuration, Nautiterm opens a new Gnome Terminal
window. To have it open a different terminal emulator, such as `Terminator`_,
add a file named ``nautiterm.yml`` in your ``$HOME/.config`` directory, with
the following contents:

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

Authors
-------

Mika Wahlroos (mika.wahlroos@iki.fi)

The code is based on `example code`_ written for the Python bindings for Nautilus
extensions.

.. _example code: https://gitlab.gnome.org/GNOME/nautilus-python/blob/master/examples/open-terminal.py
