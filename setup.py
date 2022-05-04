from openalea.deploy.metainfo import read_metainfo
from setuptools import setup, find_packages

# Reads the metainfo file
metadata = read_metainfo('metainfo.ini', verbose=True)

setup(
    name=metadata['name'],
    version=metadata['version'],
    description=metadata['description'],
    long_description=metadata['long_description'],
    author=metadata['authors'],
    author_email=metadata['authors_email'],
    url=metadata['url'],
    license=metadata['license'],
    keywords=metadata['keywords'],

    # package installation
    packages=find_packages('src'),
    package_dir={'': 'src'},

    package_data = {'':['*.csv', '*.8', '*.d3d', '*.png', '*.lsys']},
    setup_requires = ['openalea.deploy'],
    install_requires = [],
    namespace_packages=[metadata['namespace']]
)
