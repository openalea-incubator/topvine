# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys
import os

from setuptools import setup, find_packages
from openalea.deploy.metainfo import read_metainfo

name = 'OpenAlea.TopVine'
version = '1.0.0'

description = "TopVine is a package for 3D reconstruction of vine leaves."
long_description = open('README.md').read()

authors=" "
authors_email=" "

url = "https://github.com/openalea/topvine"

license = 'cecill-c'
# dependencies to other eggs
setup_requires = ['openalea.deploy']

# web sites where to find eggs
dependency_links = ['http://openalea.gforge.inria.fr/pi']

# find packages
packages = find_packages('src')
package_dir={'': 'src'}

setup(
    name=name,
    version=version,

    description=description,
    long_description=long_description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,
    keywords='vine, canopy, leaves',

    # package installation
    packages=packages,
    package_dir=package_dir,

    share_dirs={'share': 'share'},

    # Namespace packages creation by deploy
    namespace_packages=['openalea'],
    create_namespaces=True,
    zip_safe=False,

    # Dependencies
    setup_requires=setup_requires,
    dependency_links=dependency_links,


    include_package_data=True,

    # (you can provide an exclusion dictionary named exclude_package_data to remove parasites).
    # alternatively to global inclusion, list the file to include
    package_data={'': ['*.csv', '*.mtg', '*.R*', '*.ipynb']},

    # Declare scripts and wralea as entry_points (extensions) of your package
    entry_points={'wralea': ['topvine = openalea.topvine_wralea']},
    )