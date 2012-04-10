#-*- coding: utf-8 -*-
__author__ = 'chenchiyuan'

from mongoengine import *
from const import TEXT_MAX
from django.conf import settings

connect(db=settings.MONGO_DB, host=settings.DB_HOST, prot=settings.MONGO_PORT)

class Tag(Document):
    slug = StringField(max_length=TEXT_MAX, required=True)
    name_en = StringField(max_length=TEXT_MAX, required=True)
    author_slug = StringField(max_length=TEXT_MAX, default='admin')
    name_zh = StringField(map_length=TEXT_MAX)

