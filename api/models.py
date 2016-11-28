from django.db import models
from django.contrib.auth import get_user_model
from account.models import CustomUser


# User = get_user_model()


# Create your models here.
# class Author(models.Model):
#     name = models.CharField('name', max_length=100)


class Book(models.Model):
    title = models.CharField('title', max_length=100)
    author = models.CharField('Author', max_length=100)
    ISBN = models.CharField('ISBN', max_length=100)
    total_number = models.IntegerField('Total Number')
    borrowed_number = models.IntegerField('Borrowed Number', default=0)
    users = models.ManyToManyField(CustomUser)


class BorrowInformation(models.Model):
    book = models.ForeignKey('Book')
    user = models.ForeignKey(CustomUser)
    borrowed_time = models.DateTimeField()
    due_time = models.DateTimeField()
