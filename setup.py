#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# format setup arguments
from setuptools import setup, find_namespace_packages


short_descr = "3D reconstruction model of grapevine canopy"

# find version number in src/openalea/mtg/version.py
version = {}
with open("src/alinea/topvine/version.py") as fp:
    exec(fp.read(), version)

topvine_version = version["__version__"]

packages=find_namespace_packages(where='src', include=['alinea.*'])
setup_kwds = dict(
    name='alinea.topvine',
    version=topvine_version,
    description=short_descr,
    long_description=short_descr,
    author="Gaetan Louarn",
    author_email="gaetan.louarn__at__inrae.fr",
    license='cecill-c',
    zip_safe=False,

    packages=packages,
    package_dir={'': 'src'},
    entry_points={},
    keywords='',
    )
    
setup_kwds['entry_points']["wralea"] = ["topvine = alinea.topvine"]
# setup_kwds['setup_requires'] = ['openalea.deploy']


# do not change things below
setup(**setup_kwds)
