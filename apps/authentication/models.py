from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from typing import Any
from store.countries import *
from django.core.validators import MaxValueValidator


document_choices = (
    ('Citizenship', 'Citizenship'),
    ('NID', 'NID')
)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'email address',
        unique = True
    )
    first_name = models.CharField(
        'first name',
        max_length = 30,
        blank = True
    )
    last_name = models.CharField(
        'last name',
        max_length = 30,
        blank=True
    )
    date_joined = models.DateTimeField(
        'date joined',
        auto_now_add = True
    )
    is_active = models.BooleanField(
        'active',
        default = True
    )
    
    country = models.CharField(
        choices = country_choices,
        max_length = 50
    ) 
    bio = models.TextField(
        blank = True,
        null = True
    ) 
    phone_number = models.PositiveIntegerField(
        validators = [MaxValueValidator(15)]
    )
    date_of_birth = models.DateField()
    home_address = models.PointField(
        geography = True,
        default = Point(0.0, 0.0)
    )
    office_address = models.PointField(
        geography = True,
        default = Point(0.0, 0.0)
    )
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject: str, message: str, from_email: str|None = None, **kwargs: Any):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
        

class AreaOfInterest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    interest = models.CharField(max_length = 150)
    
    class Meta:
        ordering = ['-id']
        
    def __str__(self) -> str:
        return self.interest
    
    
class Document(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    document_type = models.CharField(
        choices = document_choices,
        max_length = 25
    )
    document = models.FileField(
        upload_to = 'documents/'
    )
    
    class Meta:
        ordering = ['-id']
        
    def __str__(self) -> str:
        return self.user.get_full_name