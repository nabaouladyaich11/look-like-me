from django.shortcuts import render
# django imports
from django.contrib.auth import login

# rest_framework imports
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework import status

# dj-rest-auth imports
from dj_rest_auth.serializers import LoginSerializer

# knox imports
from knox.views import LoginView, LogoutView, LogoutAllView
from knox.auth import TokenAuthentication
from django.contrib.auth.backends import ModelBackend

# local apps import
from .serializers import CustomUserDetailsSerializer
from globals.mixins import KnoxTokenOnlyMixin
        




class LoginView(LoginView):
    # login view extending KnoxLoginView
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny,]

    # rate limiting by DRF & dj-rest-auth
    throttle_scope = 'login'

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=format)

    # def get_post_response_data(self, request, token, instance):
        
    #     data = super().get_post_response_data(request, token, instance)
    #     data['user'] = CustomUserDetailsSerializer(request.user, context={'request': request}).data
    #     return data



class LogoutView(LogoutView):
    # logout view extending KnoxLogoutView

    def get_post_response(self, request):

        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)      
    


class LogoutAllView(LogoutAllView):
    # logout view extending KnoxLogoutView

    def get_post_response(self, request):

        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK) 

    # TODO define model serializer
# class ManageUserView(generics.RetrieveUpdateAPIView):
#     """Manage the authenticated user"""
#     serializer_class = UserSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_object(self):
#         """Retrieve and return authenticated user"""
#         return self.request.user
