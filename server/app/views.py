from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from app.serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


def csrf_token(request):
    """
    CSRF token view for AJAX requests.
    """
    from django.middleware.csrf import get_token
    from django.http import JsonResponse

    token = get_token(request)
    return JsonResponse({'csrfToken': token})

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # TODO: Expire 
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })