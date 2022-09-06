from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from django.db import models
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


class CustomUserFriendListView(ListView,TemplateView) :
    model = CustomUser
    serializer_class = CustomUserSerializer

    template_name = "accounts/custom_user_friend_list.html"


    def get_queryset(self , *args, **kwargs ):
        print(f"GET FRIEND_LIST_QUERYSET")
        print(f"USER = {self.request.user}")
        print(f" tofriends {self.request.user.tofriends() }")
        print(f" fromfriends {self.request.user.fromfriends() }")
        tofriends= self.request.user.tofriends()
        fromfriends= self.request.user.fromfriends()
        #if keep in ['to','all'] :
        #    print("A")
        #    queryset = list( Friend.objects.all().filter(from_user=self.request.user) ) 
        #    print("B")
        #if keep in ['from','all'] :
        #    print("C")
        #    queryset = queryset +  list( Friend.objects.all().filter(to_user=self.request.user)   )
        #    print("D")
        #if keep in ['friends'] :
        #    print("E")
        #    queryset = Friend.objects.all()
        #    print("F")

        
        qs1 =  CustomUser.objects.filter(email__in=fromfriends).annotate(todirection=(models.Value(False, output_field=models.BooleanField())))
        qs2 =  CustomUser.objects.filter(email__in=tofriends).annotate(todirection=(models.Value(True, output_field=models.BooleanField())))
        q = qs1.union( qs2  )
        return q

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context['opentahost'] =  settings.OPENTAHOST
        print(f" CONTEXT = {context}")
        return context


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
        user_context['opentahost'] = settings.OPENTAHOST
        print(f"CONTEXT = {user_context}")
        return user_context

    #def dispatch(request, *args, **kwargs):
    #    print("DISPATCH")
    #    return HttpResponse('DISPATCH')

    #def get(self, request, *args, **kwargs):
    #    return HttpResponse('GET , World!')

