"""
Crawl data from web source and parse the crawled data. 
And a backend engine that will expose a web API. 
The API can be used by client to search the data based on a specific criteria.
"""
from setuptools import setup

# python setup.py sdist
setup(name='leadbook-demo',
      version='1.0',
      license='MIT',
      description='Web Crawler & Flask API',
      long_description=__doc__,
      author='Gert Schreuder',
      url='https://github.com/gertschreuder/api-web-crawler',
      packages=['api', 'crawler'],
      entry_points={
          'console_scripts': [
              'crawler=crawler.seleniumCrawler:main'
          ]
      },
      install_requires=''
      )

__author__ = 'Gert Schreuder'
