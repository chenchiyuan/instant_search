# -*- coding: utf-8 -*-
__author__ = 'chenchiyuan'
from core.cache import cache

class SearchIndex(object):
    def __init__(self, cache_key):
        self.cache_key = cache_key

    def to_info(self):
        pass

