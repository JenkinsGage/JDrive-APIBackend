from django.contrib.auth.models import User
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from .models import File, Folder, Item


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'Items']


class FileSerializer(FlexFieldsModelSerializer):
    Size = serializers.ReadOnlyField(source='FileData.size')

    def validate_Folder(self, folder):
        if len(folder) != 1:
            raise serializers.ValidationError('File Must Be Uploaded To 1 And Only 1 Folder')
        return folder

    class Meta:
        model = File
        fields = ['Id', 'Owner', 'Name', 'UploadedTime', 'Hash', 'FileData', 'Size', 'Folder',
                  'Type']
        extra_kwargs = {
            'Owner': {'read_only': True},
            'Hash': {'read_only': True},
            'Type': {'read_only': True},
            'FileData': {'required': False},
        }


class FolderSerializer(FlexFieldsModelSerializer):

    def check_looped_folder(self, ParentFolder):
        if ParentFolder is None:
            return
        if ParentFolder == self.instance:
            raise serializers.ValidationError('Folder Dependency Is In Loop')
        if ParentFolder.ParentFolder is not None:
            self.check_looped_folder(ParentFolder.ParentFolder)

    def validate_ParentFolder(self, ParentFolder):
        if self.instance is not None and ParentFolder == self.instance:
            raise serializers.ValidationError('Parent Folder Is Not Allowed To Be Self')
        self.check_looped_folder(ParentFolder)
        return ParentFolder

    class Meta:
        model = Folder
        fields = ['Id', 'Owner', 'Name', 'CreatedTime', 'Files', 'ParentFolder', 'SubFolders',
                  'Type']
        extra_kwargs = {
            'SubFolders': {'read_only': True},
            'Owner': {'read_only': True},
            'Type': {'read_only': True},
        }

    expandable_fields = {
        'Files': (FileSerializer, {'many': True}),
        'SubFolders': ('FileShareAPI.FolderSerializer', {'many': True})
    }


class ItemSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
