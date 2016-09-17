from __future__ import unicode_literals

from django.db import models


# Create your models here.


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating ''created_ts''
    and ''updated_ts'' timestamp fields.
    """
    created_ts = models.DateTimeField('created', auto_now_add=True)
    updated_ts = models.DateTimeField('updated', auto_now=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True


class Service(models.Model):
    """
    service type defines the type of a service
    ex: resume writing, right connect etc
    nk:
    RC -> Right Connect
    PR -> Professional Services
    CS -> Combo Services
    ELS -> Executive Level Services
    """
    nk = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name
