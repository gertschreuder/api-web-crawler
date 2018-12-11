# coding: utf-8
import os

CHROME_DRIVER_PATH = r'C:\Program Files\chromedriver_win32\chromedriver.exe'

PRODUCTION = True

DATABASES = {
    'prod': {
        'ENGINE': 'mongodb',
        'NAME': 'leadbook',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    },
    'dev': {
        'ENGINE': 'mongodb',
        'NAME': 'leadbook',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '27017'
    }
}

TIME_ZONE = 'Asia/Singapore'

LANGUAGE_CODE = 'en-GB'