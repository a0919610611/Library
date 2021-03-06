from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from datetime import datetime, date


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Email is required')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if not email:
            raise ValueError('Email is required')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Username', max_length=30, unique=True, null=True)
    student_id = models.CharField('StudentId', max_length=10, blank=True, null=True)
    address = models.CharField('Address', max_length=255, blank=True, null=True)
    email = models.EmailField('Email', unique=True, null=True)
    birthday = models.DateField('BirthDay', blank=True, null=True)
    first_name = models.CharField('First name', max_length=50, default="")
    last_name = models.CharField('Last name', max_length=50, default="")
    phone_number = models.CharField('Phone Number', max_length=50, blank=True, null=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active status', default=True)
    date_joined = models.DateField('join date', auto_now_add=True)
    _unban_date = models.DateField('unban date', null=True, blank=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def unban_date(self):
        if self.is_banned:
            return self._unban_date
        else:
            return ""

    @unban_date.setter
    def unban_date(self, date):
        self._unban_date = date
        self.save()

    @property
    def is_banned(self):
        if not self._unban_date:
            return False
        return date.today() < self._unban_date

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return self.first_name + self.last_name


class BarCode(models.Model):
    bar_code = models.CharField('Bar Code', unique=True, max_length=100)
    book = models.ForeignKey('Book', null=True, blank=True, related_name='bar_codes', on_delete=models.CASCADE)
    is_borrowed = models.BooleanField('borrowed', default=False)

    def __str__(self):
        return self.bar_code


class Book(models.Model):
    title = models.CharField('title', null=True, blank=True, max_length=100)
    author = models.CharField('Author', null=True, blank=True, max_length=100)
    publisher = models.CharField('Publisher', null=True, blank=True, max_length=100)
    call_number = models.CharField('Call Number', null=True, blank=True, max_length=100)
    ISBN = models.CharField('ISBN', unique=True, null=True, blank=True, max_length=100)

    def __str__(self):
        return self.ISBN


class BorrowInfo(models.Model):
    bar_code = models.ForeignKey('BarCode', to_field='bar_code')
    username = models.ForeignKey(CustomUser, related_name='borrows', to_field='username')
    borrowed_time = models.DateField(blank=False)
    due_time = models.DateField(blank=False)
