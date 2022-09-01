from rest_framework import serializers
from django.conf import settings
from .models import CustomUser

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import Group, Permission
from friendship.models import Friend,FriendshipRequest
from rest_framework import generics
from rest_framework.decorators import action


class ChangePasswordSerializer(serializers.Serializer):

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class CustomUserSerializer(serializers.ModelSerializer):

    #related_subdomains = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('pk','id','username','email','related_subdomains','password')

    def update(self, instance , validated_data ):
        print(f" SERIALIZER UPDATE ========== {instance}")
        return super().update(instance, validated_data)


    def get_related_subdomains(self,instance):
        return instance.related_subdomains()


class CustomUserViewSet(viewsets.ModelViewSet, generics.RetrieveUpdateDestroyAPIView):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = CustomUserSerializer
    #@action(
    #        methods=["get","post","put","delete","detail"],
    #        )


    #def update(self, request , *args, **kwargs):
    #    instance = kwargs['instance']
    #    print(f"UPDATE RECORD")
    #    return Response({
    #        "is_password_updated": self.update_password(request, instance),
    #        "result": serializer.data
    #    }) 

    def get_queryset(self , *args, **kwargs ):
        print(f"GET QUERYSET")
        print(f"BASENAME = {self.basename}")
        if self.basename == 'account' :
            queryset = CustomUser.objects.filter(email=self.request.user.email)
        else :
            queryset = CustomUser.objects.all()

        #if keep in ['to','all'] :
        #    queryset = list( Friend.objects.all().filter(from_user=self.request.user) ) 
        #if keep in ['from','all'] :
        #    queryset = queryset +  list( Friend.objects.all().filter(to_user=self.request.user)   )
        #if keep in ['friends'] :
        #    queryset = Friend.objects.all()
        return queryset

    def update_password(self, request, instance):
        serializer = ChangePasswordSerializer(data = request.data)
        if serializer.is_valid():
            input_data = serializer.validated_data
            cur_password = input_data.get('current_password')
            new_password = input_data.get('new_password')
            if instance.check_password(cur_password):
                instance.set_password(new_password)
                instance.save()
                return True
        return False


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

        

#class ChangePasswordAPI(generics.UpdateAPIView):
#        """
#        An endpoint for changing password.
#        """
#        serializer_class = ChangePasswordSerializer
#        model = CustomUser
#        #permission_classes = (IsAuthenticated,)
#
#        def get_object(self, queryset=None):
#            obj = self.request.user
#            return obj
#
#        def update(self, request, *args, **kwargs):
#            self.object = self.get_object()
#            serializer = self.get_serializer(data=request.data)
#
#            if serializer.is_valid():
#                # Check old password
#                if not self.object.check_password(serializer.data.get("old_password")):
#                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#                # set_password also hashes the password that the user will get
#                self.object.set_password(serializer.data.get("new_password"))
#                self.object.save()
#                return Response("Success.", status=status.HTTP_200_OK)
#
#            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#


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
