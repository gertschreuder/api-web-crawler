# coding: utf-8
import os

PRODUCTION = True

DATABASES = {
    'docker': {
        'ENGINE': 'mongodb',
        'NAME': 'leadbook',
        'HOST': 'leadbookdb',
        'PORT': 27017
    },
    'local': {
        'ENGINE': 'mongodb',
        'NAME': 'leadbook',
        'HOST': 'localhost',
        'PORT': 27017
    }
}

TIME_ZONE = 'Asia/Singapore'

LANGUAGE_CODE = 'en-GB'
