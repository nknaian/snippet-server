import os


class Config(object):
    """Config base class"""
    CACHE_TYPE = 'FileSystemCache'
    CACHE_DIR = './.flask_caching/'
    CACHE_DEFAULT_TIMEOUT = 0
