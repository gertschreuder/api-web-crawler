from setuptools import setup

rel_path = 'README.md'

# python setup.py sdist
setup(name='leadbook-demo',
      version='1.0',
      license='MIT',
      description='Web Crawler & Flask API',
      long_description="\n" + open(rel_path).read(),
      author='Gert Schreuder',
      url='https://github.com/gertschreuder/api-web-crawler',
      packages=['api', 'crawler', 'api.data', 'api.util', 'crawler.util'],
      entry_points={
          'console_scripts': [
              'crawler=crawler.index:main',
              'api=api.app:main'
          ]
      },
      install_requires=[
        'Flask==1.0.2',
        'pymongo==2.4.1',
        'Flask_Limiter==1.0.1',
        'selenium==3.141.0']
    )

__author__ = 'Gert Schreuder'
