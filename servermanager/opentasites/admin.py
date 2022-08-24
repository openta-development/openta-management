from django.contrib import admin
from .models import OpenTASite

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


# Register your models here.

class OpenTASiteAdminForm(forms.ModelForm):

    class Meta :
        model = OpenTASite
        fields = ('id','subdomain','db_name','db_label','data')
        widgets = {
            'data': JSONEditorWidget
        }

class OpenTASiteAdmin( admin.ModelAdmin ):

    def get_readonly_fields(self, request, obj=None):
        ro_fields = super(OpenTASiteAdmin, self).get_readonly_fields(request, obj)
        if request.user.username == 'super' :
            ro_fields = ()
        return ro_fields

    def get_queryset(self,request ) :
        qs = super(OpenTASiteAdmin,self).get_queryset(request)
        for q in qs :
            try :
                if not 'description' in q.data.keys() :
                    q.data['description'] = ''
                    q.save()
            except :
                pass
        return qs


    #def get_queryset(self,request ) :
    #   qs = super(OpenTASiteAdmin,self).get_queryset(request)
    #   if request.user.username == 'super' :
    #       return qs
    #   else :
    #       return qs.filter(subdomain=settings.SUBDOMAIN)



    model = OpenTASite
    list_display = ['id','subdomain','db_name','db_label','last_activity','creator','data']
    readonly_fields =   ('id','subdomain','db_name','db_label','last_activity','creator')
    form = OpenTASiteAdminForm



#def getfirstOpenTASite() :
#    logger.debug("GET FIRRST OPENTA SITE")
#    logger.debug("SUBDOMAIN = ", settings.SUBDOMAIN)
#    obj, created = OpenTASite.objects.get_or_create(subdomain=settings.SUBDOMAIN)
#    return obj.id



admin.site.register( OpenTASite, OpenTASiteAdmin)
