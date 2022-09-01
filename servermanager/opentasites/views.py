from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from django.http import HttpResponse
from django.views.generic import ListView
from opentasites.models import OpenTASite
from rest_framework import generics
from opentasites.serializers import OpenTASiteSerializer


from django.http import HttpResponse

def index(request):
    return HttpResponse("OpenTASites - opentasites subpath ")

class OpenTASiteListView(ListView) :
    model = OpenTASite

    serializer_class = OpenTASiteSerializer

    def head(self, *arg, **wkwargs) :
        user = self.get_queryset()
        response = HttpResponse(
                    headers = {'username' : user.username }
                    )
        return response
