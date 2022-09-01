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
from accounts.serializers import CustomUserViewSet, GroupViewSet,FriendViewSet, FriendshipRequestViewSet # , ChangePasswordAPI
from opentasites.serializers import OpenTASiteViewSet
from django.contrib.auth.models import Group, Permission
from django.views.generic import TemplateView
from accounts.views import CustomUserListView, CustomUserEmailView
from opentasites.views import OpenTASiteListView




router = routers.SimpleRouter()

router.register(r'api/friends/all', FriendViewSet,basename='/')
router.register(r'api/friends/to', FriendViewSet,basename='/')
router.register(r'api/friends/from', FriendViewSet,basename='/')
router.register(r'api/friends', FriendViewSet,basename='/')
router.register(r'api/friendships_requests', FriendshipRequestViewSet,basename='/')
router.register(r'api/account', CustomUserViewSet,basename='account')
router.register(r'api/accounts', CustomUserViewSet,basename='accounts')
router.register(r'api/groups', GroupViewSet,basename='/')
router.register(r'api/opentasites/my', OpenTASiteViewSet,basename='/')
router.register(r'api/opentasites/all', OpenTASiteViewSet,basename='/')
router.register(r'api/opentasites/', OpenTASiteViewSet,basename='/')




urlpatterns = [
    path('', include(router.urls)),
    path('about/', TemplateView.as_view(template_name="about.html")),
    re_path(r'^accounts/', CustomUserListView.as_view() ),
    re_path(r'^account/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/?$', CustomUserEmailView.as_view() ),
    re_path(r'^opentasites/', OpenTASiteListView.as_view() ),
    re_path(r'^login/?$', auth_views.LoginView.as_view(template_name='registration/login.html')),
    re_path(r'^logout/?$', auth_views.LogoutView.as_view(template_name='registration/login.html')),
    re_path(r'^', include('django.contrib.auth.urls')),
    #re_path(r'^$', managerviews.main),
    path('opentasites/', include('opentasites.urls')),
    path("admin/", admin.site.urls),
    path("",  OpenTASiteListView.as_view() ),
    re_path(r"^health/?", managerviews.health ),
    path('friendship/', include('friendship.urls')),
    #re_path(r'^password-change/(?P<pk>[0-9]+)$', ChangePasswordAPI.as_view()), 
    
    ] +  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
