from rest_framework import serializers
from django.conf import settings
from .models import CustomUser

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import Group, Permission
from friendship.models import Friend,FriendshipRequest
from rest_framework import generics



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
        fields =  '__all__'

    def get_tou(self, instance):
        return instance.to_user.username

    def get_fromu(self, instance):
        return instance.from_user.username

    def get_fields(self, *args, **kwargs):
        print(f"GET_FIELDS")
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request')
        print(f" REQUEST = {request.path}")
        excludes = ['created','to_user','from_user']
        keep = request.path.split('/')[-2]
        print(f"keep = {keep}")
        if keep == 'to':
            excludes.append('fromu')
        if keep == 'from':
            excludes.append('tou')
        if request is not None and not request.parser_context.get('kwargs'):
            for  e in excludes :
                fields.pop(e,None)
        return fields

        



class FriendViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = FriendSerializer

    def get_queryset(self , *args, **kwargs ):
        print(f"FriendViewSet {self.request.path}")
        keep = self.request.path.split('/')[-2]
        print(f"keep2 = {keep}")
        queryset = []
        if keep in ['to','all'] :
            queryset = list( Friend.objects.all().filter(from_user=self.request.user) ) 
        if keep in ['from','all'] :
            queryset = queryset +  list( Friend.objects.all().filter(to_user=self.request.user)   )
        if keep in ['friends'] :
            queryset = Friend.objects.all()
        return queryset


class FriendshipRequestSerializer(serializers.ModelSerializer):

    tou = serializers.SerializerMethodField()
    fromu = serializers.SerializerMethodField()


    class Meta:
        model = FriendshipRequest
        fields = ('fromu','tou','message')

    def get_tou(self, instance):
        return instance.to_user.username

    def get_fromu(self, instance):
        return instance.from_user.username
        



class FriendshipRequestViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = FriendshipRequestSerializer
    queryset = FriendshipRequest.objects.all()
