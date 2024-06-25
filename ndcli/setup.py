from setuptools import setup
from dimcli import version

setup(name='ndcli',
      version=version.VERSION,
      scripts=['ndcli'],
      install_requires=['dimclient>=0.4.1',
                        'python-dateutil',
                        'dnspython'],
      packages=['dimcli'])
