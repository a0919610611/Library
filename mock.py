#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, django
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Library.settings")

django.setup()
from api.models import Book

Book.objects.create(title="test1", author="author1", publisher="pub1", call_number="123", ISBN='1234567')
Book.objects.create(title="test12", author="author1", publisher="pub1", call_number="123", ISBN='2')
Book.objects.create(title="test123", author="author1", publisher="pub1", call_number="123", ISBN='3')
