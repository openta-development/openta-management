from django.contrib.auth.hashers import make_password
from django.db.models.base import ObjectDoesNotExist 
from email.utils import parseaddr
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
from friendship.models import Friend,FriendshipRequest
from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument( '--dry-run', dest='dry-run', default="True", help='specify if dry-run.')



    def handle(self, *args, **kwargs):
        dry_run = ( kwargs.get('dry-run') ).lower() == 'true'
        MAKE_FRIENDS = True
        MAKE_USERS = True
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
        if MAKE_USERS :
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
        bogus = ['super@gmail.com','test@test.se']
        for email in all_emails :
            first_part = email.split('@')[0]
            last_part = email.split('@')[1].split('.')
            if first_part and len( last_part) >  1  and not 'super' in first_part :
                print(f" OK {email} ")
            else :
                bogus = bogus + [email]
                print(f" NOK {email}")

        if MAKE_FRIENDS :
            for o in opentasites :
                data = o.data
                try :
                    superusers = data['superusers']
                    for i in range(1,len(superusers) ):
                        for j in range(0,i):
                            e1 = superusers[i]['email']
                            e2 = superusers[j]['email']
                            if not e1 in bogus and not e2 in bogus :
                                u1 = CustomUser.objects.get(email=e1)
                                u2 = CustomUser.objects.get(email=e2)
                                try :
                                    Friend.objects.add_friend(u1,u2)
                                except AlreadyFriendsError as e:
                                    #print(f"Error = {type(e).__name__}")
                                    pass
                                try :
                                    friend_request = FriendshipRequest.objects.get(from_user=u1, to_user=u2)
                                    friend_request.accept()
                                except ObjectDoesNotExist as e:
                                    pass
                                except Exception as e :
                                    print(f" ERROR 18993 {type(e).__name__}")

                except Exception as e:
                    print(f" ERROR 9227 {type(e).__name__} {str(e)} ")

