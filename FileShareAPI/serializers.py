from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from .models import File, Folder, Share

UserModel = get_user_model()


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'Items']
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'required': True},
            'Items': {'read_only': True}
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'])
        return user


class FileSerializer(FlexFieldsModelSerializer):
    Size = serializers.ReadOnlyField(source='FileData.size')

    class Meta:
        model = File
        fields = ['Id', 'Owner', 'Name', 'UploadedTime', 'Hash', 'FileData', 'Size', 'ParentFolder',
                  'Type', 'Creator']
        extra_kwargs = {
            'Owner': {'read_only': True},
            'Hash': {'read_only': True},
            'Type': {'read_only': True},
            'FileData': {'required': False},
            'Creator': {'read_only': True}
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
                  'Type', 'Creator']
        extra_kwargs = {
            'SubFolders': {'read_only': True},
            'Owner': {'read_only': True},
            'Type': {'read_only': True},
            'Creator': {'read_only': True}
        }

    expandable_fields = {
        'Files': (FileSerializer, {'many': True}),
        'SubFolders': ('FileShareAPI.FolderSerializer', {'many': True})
    }


class ShareSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'
        extra_kwargs = {
            'Id': {'read_only': True},
            'Owner': {'read_only': True},
            'Code': {'write_only': True},
            'Items': {'read_only': True}
        }
