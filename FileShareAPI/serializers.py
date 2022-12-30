from django.contrib.auth.models import User
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from .models import File, Folder, Item


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'Items', 'AccessibleItems']


class FileSerializer(FlexFieldsModelSerializer):
    Size = serializers.ReadOnlyField(source='FileData.size')

    class Meta:
        model = File
        fields = ['Id', 'Owner', 'Name', 'Access', 'IsSharable', 'UploadedTime', 'Hash', 'FileData', 'Size', 'Folder']
        extra_kwargs = {
            'Owner': {'read_only': True},
            'Name': {'read_only': True},
            'Hash': {'read_only': True}
        }


class FolderSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Folder
        fields = ['Id', 'Owner', 'Name', 'Access', 'IsSharable', 'CreatedTime', 'Files', 'ParentFolder', 'SubFolders']
        extra_kwargs = {
            'SubFolders': {'read_only': True},
            'Owner': {'read_only': True}
        }

    expandable_fields = {
        'Files': (FileSerializer, {'many': True}),
        'SubFolders': ('FileShareAPI.FolderSerializer', {'many': True})
    }


class ItemSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
