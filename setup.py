from setuptools import setup, find_packages
import os.path

# allows specifying encoding for open() in both Python 2 and 3
from io import open

# based on the packaging sample project at
# https://github.com/pypa/sampleproject/blob/master/setup.py

here = os.path.abspath(os.path.dirname(__file__))


def _read_long_description():
    readme_path = os.path.join(here, 'README.rst')
    with open(readme_path, encoding='utf-8') as f:
        return f.read()


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

    zip_safe=True
)
