from setuptools import setup
from cas import version

# python can't handle the fact, that data_files might contain directories.
# So we have to split off every directory into its own data_files statement
# with all its files just to make this work.
data_files = []
data_files.append(('share/dim-cas', ['cas.wsgi', 'cas/config.py.example']))

setup(name='dim-cas',
      packages=['cas'],
      data_files = data_files,
      version=version.VERSION,
      install_requires=['xmltodict', 'flask', 'requests'])
