from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Employee(models.Model):
    user = models.OneToOneField(User)
    salarium_password = models.CharField(max_length=100)

    def __unicode__(self):
        return self.user.username
