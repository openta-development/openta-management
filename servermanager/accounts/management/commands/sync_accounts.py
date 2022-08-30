from django.contrib.auth.hashers import make_password
import datetime
import json
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
import logging
from opentasites.models import OpenTASite
from django.conf import settings
import glob
import re
from django.db import connections, connection
from accounts.models import CustomUser

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument( '--dry-run', dest='dry-run', default="True", help='specify if dry-run.')



    def handle(self, *args, **kwargs):
        dry_run = ( kwargs.get('dry-run') ).lower() == 'true'
        opentasites  =  OpenTASite.objects.using('opentasites').all()
        all_superusers = []
        for o in opentasites :
           #print(f"subdomain = {o.subdomain} {o.creator} ")
           try :
             data = o.data
             all_superusers = all_superusers + data['superusers']
           except:
              #print(f" SUBDOMAIN {o.subdomain} has no superuser")
              pass
        #print(f" ALL superusers = {all_superusers}")
        all_emails = list( set( [item['email'] for item in all_superusers ] ))
        #print(f" ALL EMAILS = {all_emails}")
        passwords = {}
        for email in all_emails :
           #print(f"EMAIL = {email}")
           a = [ item for item in all_superusers if item['email'] == email ]
           dd = sorted( a , key = lambda item: item['last_login'] )
           #for d in dd :
           #    print(f"d = {d}")
           passwords[email] = dd[-1]['password']
        for user in  passwords.keys():
            p = passwords[user]
            if not p :
                p = make_password( user )
            print(f"{user} {p}")
            if not dry_run :
                account, _ = CustomUser.objects.get_or_create(email=user)
                account.password = p
                account.username = user
                account.save()
                print(f"updated {user}")
            else :
                print(f"would update {user}")

        
