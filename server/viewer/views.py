from django.shortcuts import render
from rest_framework import permissions, viewsets
from viewer.serializers import DirectorySerializer, StlSerializer
from viewer.models import DIRECTORY,STL


class DirectoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DIRECTORY.objects.all()
    serializer_class = DirectorySerializer
    permission_classes = [permissions.IsAuthenticated]


class StlViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset           = STL.objects.all()
    serializer_class   = StlSerializer
    permission_classes = [permissions.IsAuthenticated]

    
    