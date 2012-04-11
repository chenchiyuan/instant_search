# -*- coding: utf-8 -*-
__author__ = 'chenchiyuan'
from core.cache import cache
from core.const import SEARCH_KEY_PREFIX
from mmseg import seg_txt
import logging
logger = logging.getLogger(__file__)

class SearchIndex(object):
    def __init__(self):
        self.cache_key_prefix = SEARCH_KEY_PREFIX

    def to_info(self):
        pass

    def parse(self, words):
        results = [word for word in seg_txt(words)]
        return filter(None, results)


    def add(self, word, key, score):
        try:
            cache.zadd(self.cache_key_prefix + word , key= key, score=score)
        except:
            logger.debug("cannot add search index key: %s score: %s" %(key, score))

    def get(self, word):
        try:
            return cache.zrevrangebyscore(name=self.cache_key_prefix + word, max='+inf', min="-inf")
        except Exception as err:
            logger("cache_key %s for err %s" %(cache_key, err))
            return None

    def score(self, words):
        will_scores = self.parse(words)


    def search(self, words):
        if cache.exists(self.cache_key_prefix + words):
            return {
                words: self.get(words)
            }

        keys = [(self.cache_key_prefix + word) for word in seg_txt(words)]
        try:
            cache.zinterstore(words, keys)
        except:
            return None

        cache_keys = cache.zrevrangebyscore(words, "+inf", "-inf")
        tags = []
        for cache_key in cache_keys:
            tags.append(self.get(cache_key))
        tags = filter(None, tags)
        return {
            words: tags
        }

if __name__ == '__main__':
    print("success")