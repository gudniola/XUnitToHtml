#!/usr/bin/env python

from distutils.core import setup

setup(name='XUnit2HTML',
      version='1.0.1',
      description='A tool for converting xunit generated xml files into an html report',
      author='Gudni Olafsson',
      author_email='gudni.olafsson@gmail.com',
      py_modules=['xunit2html'],
      scripts=['src/x2h.py'],
      packages=[''],
      package_dir={'': 'src'},
      package_data={'': ['templates/*.tmpl', 'templates/jquery-1.9.1.min.js', 'templates/report.css']},
      requires=['argparse'])
