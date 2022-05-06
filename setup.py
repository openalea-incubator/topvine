import sys, os
from setuptools import setup, find_packages
from os.path import join as pj

from openalea.deploy.metainfo import read_metainfo

# Reads the metainfo file
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))


setup(name = name,
      version = version,
      description = description,
      long_description = long_description,
      authors = authors,
      authors_email = authors_email,
      license = license,
      namespace_packages = [namespace], 
      create_namespaces = True,
      #packages = [pkg_name],
      zip_safe = False,
      packages =  [ 'alinea.topvine',
                    'alinea.topvine.carto',
                    'alinea.topvine.demo',
                    'alinea.topvine.macro',
			  'alinea.topvine.farquhar',
			  'alinea.topvine.farquhar.demo',
                    'alinea.topvine.lsystem',
                    'alinea.topvine.geom',
                    'alinea.topvine.farquhar',
                    'alinea.topvine.farquhar.demo',
                    'alinea.topvine.farquhar.macro',
                    'alinea.topvine.law',
                    'alinea.topvine.rammoy',
                    'alinea.topvine.digit',
                    'alinea.topvine.data'  ],

      package_dir = { 'alinea.topvine':  'topvine', },
      package_data = {'':['*.csv', '*.8', '*.d3d', '*.png', '*.lsys']},
      entry_points = { 'wralea': [ 'topvine = alinea.topvine',] },

      # Dependencies
      setup_requires = ['openalea.deploy'],
      install_requires = [],
      dependency_links = ['http://openalea.gforge.inria.fr/pi'],
)

