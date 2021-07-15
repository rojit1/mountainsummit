from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, type, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,type=type, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, type, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, type, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USER_TYPES = [
        ('ORGANIZATION','Organization'),
        ('USER', 'User'),
        ('S','s')
    ]
    type = models.CharField(max_length=20,choices=USER_TYPES, default='USER')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['type']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

        

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    website = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        if self.name:
            return self.name
        if self.firstname and self.lastname:
            return self.firstname+' '+self.lastname
        return self.user.email
