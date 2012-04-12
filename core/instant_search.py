# -*- coding: utf-8 -*-
__author__ = 'chenchiyuan'
from core.cache import cache
from core.const import SEARCH_KEY_PREFIX
from mmseg import seg_txt
from django.template.defaultfilters import slugify
from unidecode import unidecode
import logging
logger = logging.getLogger('default')

class SearchIndex(object):
    def __init__(self):
        self.cache_key_prefix = SEARCH_KEY_PREFIX

    @staticmethod
    def __to_unicode(word):
        if isinstance(word, (unicode, type(None))):
            return word
        try:
            return unicode(word, 'utf-8')
        except:
            logger.debug("cannot unicode word %s" %word)
            return None

    @staticmethod
    def score(word):
        logger.debug("will score a word %s" %word)

    def to_info(self):
        pass

    def parse(self, words):
        _seg_words = [word for word in seg_txt(words)]
        seg_words = filter(None, _seg_words)
        results = []
        for word in seg_words:
            word_utf8 = SearchIndex.__to_unicode(word)
            decode_word = unidecode(word_utf8)
            key = self.cache_key_prefix + slugify(decode_word)
            results.append(key)
        return results


    def add(self, word, key, score):
        try:
            cache.zadd(self.cache_key_prefix + word , key= key, score=score)
        except:
            logger.debug("cannot add search index key: %s score: %s" %(key, score))

    def get(self, word):
        try:
            return cache.zrevrangebyscore(name=self.cache_key_prefix + word, max='+inf', min="-inf")
        except Exception as err:
            logger("cache_key %s for err %s" %(self.cache_key_prefix + word, err))
            return None

    def search(self, words):
        keys = self.parse(words)
        print(keys)
        try:
            cache.zinterstore(words, keys)
        except Exception as err:
            logger.error("Err is %s" %err)
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