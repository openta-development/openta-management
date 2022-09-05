from django.db import models

# Create your models here.

import logging
from django.db import models
import uuid
from django_json_widget.widgets import JSONEditorWidget
from django import forms
from django.conf import settings
#from django.contrib.sites.models import Site
from django.db.models import JSONField
from django.contrib import admin
import random
from django.conf import settings

logger = logging.getLogger(__name__)


def random_db_name( subdomain ):
    return "%s-%s" % ( str( subdomain ), random.randint(10000,99999) )

class OpenTASite(models.Model ):

    subdomain = models.CharField(max_length=4096, editable=True)
    course_key = models.CharField(max_length=4096,  default='', editable=True)
    db_name = models.CharField(max_length=4096,  editable=True)
    db_label= models.CharField(max_length=4096,  default='', editable=True)
    creator = models.CharField(max_length=4096,  default='', editable=True)
    last_activity = models.DateTimeField(auto_now=True)
    data = JSONField(default=dict)

    #objects = models.Manager()

    class Meta:
        unique_together = ("subdomain", "course_key")
        #constraints = [ models.UniqueConstraint(fields=['db_name'],name="Database must be unique" ),
        #                models.UniqueConstraint(fields=['subdomain'],name="Subdomain value must be unique" ) ]
                        

    def __str__(self):
        return self.subdomain

    def save(self, *args, **kwargs):
        logger.debug("SAVING MODEL %s " %  self.subdomain)
        if self.db_name is None:
            self.db_name = self.subdomain + '-' + str( random.randint( 11111,99999) )
        if self.db_label is None:
            self.db_name = self.subdomain
        super(OpenTASite, self).save(*args, **kwargs)

    #def getSite(self ):
    #    return Site.objects.get_or_create(name=self.subdomain)



