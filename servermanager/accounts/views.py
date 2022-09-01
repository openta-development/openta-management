from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from django.http import HttpResponse
from django.views.generic import ListView
from accounts.models import CustomUser
from rest_framework import generics
from accounts.serializers import CustomUserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'accounts': reverse('accounts-list', request=request, format=format),
    })

class CustomUserHighlight(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        custom_user = self.get_object()
        return Response(custom_user.highlighted)


class CustomUserListView(ListView) :
    model = CustomUser

    serializer_class = CustomUserSerializer

    def head(self, *arg, **wkwargs) :
        user = self.get_queryset()
        response = HttpResponse(
                    headers = {'username' : user.username }
                    )
        return response
