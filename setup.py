import codecs
from distutils.core import setup

from setuptools import find_packages

with codecs.open("readme.MD", "r", "utf-8") as fd:

    setup(
        name='ptbtest',
        version='1.3',
        packages=['ptbtest'],
        url='https://github.com/Eldinnie/ptbtest',
        license='GNU General Public License v3.0',
        author='Pieter Schutz',
        author_email='pieter.schutz@gmail.com',
        description='A testsuit for use with python-telegram-bot',
        long_description=fd.read(),
        install_requires=['python-telegram-bot'],
        keywords='python telegram bot unittest',
        classifiers=[
                  'Development Status :: 4 - Beta',
                  'Intended Audience :: Developers',
                  'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                  'Operating System :: OS Independent',
                  'Topic :: Software Development :: Libraries :: Python Modules',
                  'Topic :: Software Development :: Testing',
                  'Topic :: Internet',
                  'Programming Language :: Python',
                  'Programming Language :: Python :: 2',
                  'Programming Language :: Python :: 2.7',
                  'Programming Language :: Python :: 3',
                  'Programming Language :: Python :: 3.3',
                  'Programming Language :: Python :: 3.4',
                  'Programming Language :: Python :: 3.5',
                  'Programming Language :: Python :: 3.6'
              ],
    )
