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

    request_username = forms.CharField()
    

    class Meta :
        model = OpenTASite
        fields = ('id','subdomain','db_name','db_label','data','request_username')
        widgets = {
            'data': JSONEditorWidget
        }

class OpenTASiteAdmin( admin.ModelAdmin ):

    form = OpenTASiteAdminForm
    model = OpenTASite
    list_display = ['id','subdomain','db_name','db_label','last_activity','creator','data']
    readonly_fields =   ('id','subdomain','db_name','db_label','last_activity','creator')
    form = OpenTASiteAdminForm


    def get_readonly_fields(self, request, obj=None):
        ro_fields = super(OpenTASiteAdmin, self).get_readonly_fields(request, obj)
        print(f"GET READONLY FIELDS")
        if request.user.username == 'super' :
            ro_fields = ()
        return ro_fields

    def get_queryset(self,request ) :
        print(f"ADMIN GET QUERYSET")
        qs = super(OpenTASiteAdmin,self).get_queryset(request)
        for q in qs :
            try :
                if not 'description' in q.data.keys() :
                    q.data['description'] = ''
                    q.save()
            except :
                pass
        return qs

    def get_form(self, request, obj=None, **kwargs):
        print(f" ADMIN GET FORM ")
        form = super().get_form(request, obj, **kwargs)
        if not 'request_username' in form.base_fields :
            form.base_fields['request_username'] = forms.fields.CharField()
        form.base_fields['request_username'].initial = request.user.username # THIS IS WHERE request_username is set
        return form



#def getfirstOpenTASite() :
#    logger.debug("GET FIRRST OPENTA SITE")
#    logger.debug("SUBDOMAIN = ", settings.SUBDOMAIN)
#    obj, created = OpenTASite.objects.get_or_create(subdomain=settings.SUBDOMAIN)
#    return obj.id



admin.site.register( OpenTASite, OpenTASiteAdmin)
