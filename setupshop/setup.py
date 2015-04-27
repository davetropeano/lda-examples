from setuptools import setup
import multiprocessing

setup(name='setupshop',
      version='1.0',
      description='On-line Store Hosting Example',
      author='Your Name',
      author_email='example@example.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=[#'ld4apps>='0.9',
                        'requests>=0.14.1', 
                        'webob>=1.2.3', 
                        'pycrypto>=2.6',
                        'pymongo>=2.4.1',
                        'isodate>=0.4.9', 
                        'python-dateutil>=2.1',
                        'rdflib>=3.2.2',
                        'PyJWT>=0.1.6',
                        'werkzeug>=0.9.4']
     )
