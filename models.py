# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(null=True, blank=True)
    password_token = models.CharField(max_length=32, null=True, blank=True)

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name