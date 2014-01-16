'''
Created on Jan 14, 2014

@author: ivan
'''
import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

pkg_def=os.path.join(os.path.split(__file__)[0], 'unistego', '__init__.py')
m=re.search(r'__version__\s*=\s*(.*)', open(pkg_def, 'rt').read())
version=eval(m.group(1))
version = '.'.join(map(lambda s: str(s), version))

setup(name='unistego',
      version=version,
      description='Python unicode steganography',
      packages=['unistego'],
      author='Ivan Zderadicka',
      author_email='ivan.zderadicka@gmail.com',
      requires= ['six (>=1.4.1)', 'bitarray (>=0.8.1)'],
      install_requires=['six>=1.4.1', 'bitarray>=0.8.1'],
      provides=['unistego'],
      scripts=['unistego-tool']
      )