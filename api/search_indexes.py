#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from api.models import Book
from haystack import indexes


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    author = indexes.CharField(model_attr='author')
    ISBN = indexes.CharField(model_attr='ISBN')

    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
