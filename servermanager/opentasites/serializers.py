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
    queryset = OpenTASite.objects.all()

