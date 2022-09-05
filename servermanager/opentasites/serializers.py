from rest_framework import serializers
from django.conf import settings
from .models import OpenTASite

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

class OpenTASiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpenTASite
        fields = '__all__'


class OpenTASiteViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = OpenTASiteSerializer

    def get_queryset(self , *args, **kwargs ):
        keep = self.request.path.split('/')[-2]
        if keep == 'my' :
            queryset = OpenTASite.objects.filter(creator=self.request.user.email)
        else :
            queryset = OpenTASite.objects.all()
        #subdomains = self.request.user.related_subdomains()
        #if keep in ['to','all'] :
        #    queryset = list( Friend.objects.all().filter(from_user=self.request.user) ) 
        #if keep in ['from','all'] :
        #    queryset = queryset +  list( Friend.objects.all().filter(to_user=self.request.user)   )
        #if keep in ['friends'] :
        #    queryset = Friend.objects.all()
        return queryset


