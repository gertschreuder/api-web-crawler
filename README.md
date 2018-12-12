# Python Web Crawler & Flask API
## Crawl data from web source and parse the crawled data. And a backend engine that will expose a web API. The API can be used by client to search the data based on a specific criteria
---
## Prerequisits
* [Chrome Driver for Windows](https://sites.google.com/a/chromium.org/chromedriver/downloads)
    * If you are running a Linux OS you can [read more here](https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/)
* [Docker Community Edition](https://docs.docker.com/docker-for-windows/install/)
    * If you are running docker on Windows ensure that you are running Docker Linux containers
* [Docker Compose](https://docs.docker.com/compose/install/)
* We will need a tool named postman to test our APIs. You can download it from [here](https://www.getpostman.com/apps)
* [Python 3.6](https://www.python.org/downloads/release/python-360/)
* [Pip](https://pip.pypa.io/en/stable/installing/)
---
## Crawler
* Run the following command in the project root folder
  * python -m pip install selenium==3.141.0
  * python .\crawler\index.py

---
## API
To start the Flask API, cd into .\api folder and execute the following commands:
* docker-compose build
* docker-compose up
---
## Tests
* Import the .\tests\postman\leadbook.postman_collection.json into Postman app to test the api methods
