from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    """
    By default, the "get_object()" returns a specific object using its primary
    key ID in the URL, like "/profile/<id>/", i.e., it doesn't return the
    authenticated user. The default function will return the object with the
    ID provided in the URL. We override this to always return the
    authenticated user.
    """

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
