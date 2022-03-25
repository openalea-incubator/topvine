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

    # Namespace packages creation by deploy
    namespace_packages=[metadata['namespace']],
    create_namespaces=True,
    zip_safe=False,

    # Dependencies
    setup_requires=['openalea.deploy'],
    dependency_links=['http://openalea.gforge.inria.fr/pi'],
    install_requires=[]
)
