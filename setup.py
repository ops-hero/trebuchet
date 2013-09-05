#!/usr/bin/env python
from setuptools import setup, find_packages

from trebuchet.lib import get_version

setup(
    name = "Trebuchet",
    packages = find_packages(),
    version = get_version(),
    url = '',
    author = 'Arnaud Seilles',
    author_email = 'arnaud.seilles@gmail.com',
    description = "Yet another package building tool",
    long_description="Yet another package building tool",
    include_package_data = True,
    entry_points = {
        "console_scripts" : [ "trebuchet = "
            "trebuchet.run:main"]
    },
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Environment :: Web',
                   'License :: OSI Approved :: GNU Affero General Public License v3',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
    install_requires = open('requirements.pip').readlines(),
    dependency_links = ["http://c.pypi.python.org/simple"],
)
