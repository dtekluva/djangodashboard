# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
       
class SecondUser(models.Model):
    phone_number = models.CharField(max_length=20, default="0")
    is_ceo = models.BooleanField(default=False)
    is_ppl_staff = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

   