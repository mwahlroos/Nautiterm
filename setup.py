from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import os.path

# Allows specifying encoding for open() in both Python 2 and 3
from io import open

# Based on the packaging sample project at
# https://github.com/pypa/sampleproject/blob/master/setup.py

here = os.path.abspath(os.path.dirname(__file__))


def _read_long_description():
    readme_path = os.path.join(here, 'README.rst')
    with open(readme_path, encoding='utf-8') as f:
        return f.read()


# Install stanza based on that of nautilus-terminal by Fabien Loison;
# https://github.com/flozz/nautilus-terminal/blob/master/setup.py
class install(_install):
    def run(self):
        print("--- Installing Nautiterm Python package in site-packages")
        _install.run(self)

        # copy the extension file to the Nautilus Python extensions dir
        src_file = "src/nautiterm/open_terminal.py"
        dst_dir = os.path.join(self.install_data, "share/nautilus-python/extensions")
        self.mkpath(dst_dir)
        dst_file = os.path.join(dst_dir, os.path.basename(src_file))
        print("--- Installing Nautilus extension in " + dst_dir)
        if os.path.exists(dst_file):
            print("--- File {f} already exists; skipping".format(f=dst_file))
        else:
            self.copy_file(src_file, dst_file)


setup(
    name='Nautiterm',
    version='0.0.1',

    description='Nautilus extension for opening a configurable terminal at the current location',
    long_description=_read_long_description(),
    long_description_content_type='text/x-rst',

    package_dir={'': 'src'},
    packages=find_packages(),

    author='Mika Wahlroos',
    author_email='mika.wahlroos@iki.fi',
    url='https://github.com/mwahlroos/Nautiterm',
    license='GNU General Public License v2 (GPLv2)',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: X11 Applications :: Gnome',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords=['Nautilus', 'Terminal', 'Terminator'],

    python_requires='>= 2.7, != 3.0.*, != 3.1.*, != 3.2.*, != 3.3.*',
    install_requires=[
        'PyGObject >= 3.28',
        'pyyaml >= 3.13'
    ],

    zip_safe=True,

    # use the custom install routine
    cmdclass={"install": install}
)
