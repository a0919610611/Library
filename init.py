#!/usr/bin/env python3
import os,django
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Library.settings")

django.setup()
from api.models import CustomUser

try:
    CustomUser.objects.create_superuser("admin","admin@admin.com","12345678")
except:
    print("admin exists")
