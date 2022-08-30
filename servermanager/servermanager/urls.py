"""servermanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from rest_framework import routers

from django.contrib import admin
from django.urls import path
from django.urls import include, path
from servermanager import views as managerviews
from django.urls import re_path 
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts.serializers import CustomUserViewSet, GroupViewSet,FriendViewSet
from opentasites.serializers import OpenTASiteViewSet
from django.contrib.auth.models import Group, Permission


router = routers.SimpleRouter()

router.register(r'friends', FriendViewSet)
router.register(r'accounts', CustomUserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'opentasites', OpenTASiteViewSet)




urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^login/?$', auth_views.LoginView.as_view(template_name='registration/login.html')),
    re_path(r'^logout/?$', auth_views.LogoutView.as_view(template_name='registration/login.html')),
    re_path(r'^', include('django.contrib.auth.urls')),
    re_path(r'^$', managerviews.main),
    path('opentasites/', include('opentasites.urls')),
    path("admin/", admin.site.urls),
    path("", managerviews.main ),
    path('change-password/', auth_views.PasswordChangeView.as_view()),
    re_path(r"^health/?", managerviews.health ),
    path('friendship/', include('friendship.urls'))
    ] +  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
