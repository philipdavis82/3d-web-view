from django.shortcuts import render
from rest_framework import permissions, viewsets
from viewer.serializers import DirectorySerializer, StlSerializer
from viewer.models import DIRECTORY,STL
from django.db import models

class DirectoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DIRECTORY.objects.all()
    serializer_class = DirectorySerializer
    permission_classes = [permissions.IsAuthenticated]


class StlViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset           = STL.objects.all()
    serializer_class   = StlSerializer
    permission_classes = [permissions.IsAuthenticated]

    
class StlByNameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset           = STL.objects.all()
    serializer_class   = StlSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        name_ = self.kwargs['name']
        objs = STL.objects.filter(name=models.CharField(name_))
        print("STL Name Query: ",name_,objs)
        return objs


class StlByParentIdViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset           = STL.objects.all()
    serializer_class   = StlSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        dirid_ = self.kwargs['dirid']
        objs = STL.objects.filter(dirid=dirid_)
        print("STL Name Query: ",dirid_,objs)
        return objs


class DirByParentIdViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset           = DIRECTORY.objects.all()
    serializer_class   = DirectorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        dirid_ = self.kwargs['dirid']
        objs = DIRECTORY.objects.filter(dirid=dirid_)
        print("DIR Name Query: ",dirid_,objs)
        return objs

from django.http import FileResponse
from django.shortcuts import get_object_or_404

def get_stl_file(request, id):
    """
    Serves the .STL file associated with a model instance.
    """
    instance = get_object_or_404(STL, id=id)  # Or however you identify your file
    file_path = instance.path  # Assuming your model has an stl_file field

    response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{instance.name}"' # optional
    return response