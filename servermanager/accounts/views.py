from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from accounts.models import CustomUser
from rest_framework import generics
from accounts.serializers import CustomUserSerializer
from django.views import View
from django.views.generic.detail import DetailView




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


class CustomUserEmailView(TemplateView) :

    model = CustomUser
    serializer_class = CustomUserSerializer

    template_name = "accounts/custom_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email = context['email']
        user = CustomUser.objects.get(email=email)
        print(f"USER = {user}")
        user_context = CustomUserSerializer(user).data
        print(f"CONTEXT = {user_context}")
        return user_context

    #def dispatch(request, *args, **kwargs):
    #    print("DISPATCH")
    #    return HttpResponse('DISPATCH')

    #def get(self, request, *args, **kwargs):
    #    return HttpResponse('GET , World!')

