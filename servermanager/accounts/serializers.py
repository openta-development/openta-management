from rest_framework import serializers
from django.conf import settings
from .models import CustomUser

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import Group, Permission
from friendship.models import Friend,FriendshipRequest



class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class GroupViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

class FriendSerializer(serializers.ModelSerializer):

    tou = serializers.SerializerMethodField()
    fromu = serializers.SerializerMethodField()


    class Meta:
        model = Friend
        fields = ('fromu','tou',)

    def get_tou(self, instance):
        print(f"INSTANCE =  {instance.to_user} {instance.from_user} ")
        return instance.to_user.username

    def get_fromu(self, instance):
        return instance.from_user.username
        



class FriendViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()
