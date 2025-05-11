from viewer.models import DIRECTORY,STL
from rest_framework import serializers


class DirectorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = DIRECTORY
        fields = ['id','path', 'name', 'dir', 'dirid']


class StlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = STL
        fields = ['id','path', 'name', 'dir', 'icon', 'prev', 'dirid']