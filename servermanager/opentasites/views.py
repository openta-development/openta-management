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

    #def head(self, *arg, **wkwargs) :
    #    user = self.get_queryset()
    #    response = HttpResponse(
    #                headers = {'username' : user.username }
    #                )
    #    return response


    def get_context_data(self, **kwargs):
        c = super(OpenTASiteListView, self).get_context_data(**kwargs)
        if "sort_by" in self.request.GET:
            c["current_sort_field"] = self.request.GET.get("sort_by")
        return c

    def get_queryset(self):
        # apply sorting
        qs = super(OpenTASiteListView, self).get_queryset()
        if "sort_by" in self.request.GET:
            qs = qs.order_by(self.request.GET.get("sort_by"))
        return qs
