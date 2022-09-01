from django.db import models
from django.conf import settings
from django.contrib import admin
from django.db.models.signals import  post_save, pre_delete
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from opentasites.models import OpenTASite
from django.contrib.postgres.fields import CICharField, CIEmailField
from django.core.mail import send_mail
from django.db import models
from django.dispatch import Signal, receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save(sender, instance, created, **kwargs):
    email = instance.email
    signal = kwargs['signal']
    print(f"PASSWSORD = {instance.password}")
    subdomains = instance.related_subdomains()
    for subdomain in subdomains:
        print(f" subdomain = {subdomain}")
        o = OpenTASite.objects.get(subdomain=subdomain)
        print(f" data = {o.data}")
        superusers = o.data['superusers']
        for u in superusers :
            if u['email'] == email :
                u['password'] = instance.password
        o.save()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = ASCIIUsernameValidator()

    username = CICharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = CIEmailField(
        _("email address"),
        unique=False,
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    #def post_save(self, *args, **kwargs):
    #    logger.error(f"POST SAVE USER")


    def save(self, *args, **kwargs):
        print(f"SAVE USER")
        super().save(*args, **kwargs) 


    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def related_subdomains( self ):
        qs = list( OpenTASite.objects.all().values_list('subdomain','data') )
        r = []
        for q in qs :
            try :
                if q[1]['creator'] == self.email :
                    r.append( q[0] )
                #print(f" Q = {q[0]} {q[1]['creator']}")
                for s in q[1]['superusers'] :
                    if s['email'] == self.email :
                        r.append( q[0] )
                    #print(f"S { q[0] } {s['email']}")
            except: 
                pass
        r = list( set(r))
        r.sort()
        return r

admin.site.register(CustomUser)
