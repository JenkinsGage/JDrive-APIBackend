import mimetypes

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_flex_fields import FlexFieldsModelViewSet, is_expanded
from rest_framework import permissions, generics

from .models import File, Folder
from .serializers import UserSerializer, FolderSerializer, FileSerializer, RegisterSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response


class FileList(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(Owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(Owner=user)


class FileByHash(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(Hash=self.request.query_params['Hash'])


class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(Q(Owner=user))


class FolderList(generics.ListCreateAPIView):
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Folder.objects.filter(Q(Owner=user))

    def perform_create(self, serializer):
        serializer.save(Owner=self.request.user)


class FolderRoot(generics.ListAPIView, FlexFieldsModelViewSet):
    permit_list_expands = ['Files', 'SubFolders']
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # for optimization purpose we prefetch expands area to reduce the database hits
        expands = [x for x in self.permit_list_expands if is_expanded(self.request, x)]
        if expands:
            return Folder.objects.filter(Q(Owner=user) & Q(ParentFolder=None)).prefetch_related(*expands)
        ##

        return Folder.objects.filter(Q(Owner=user) & Q(ParentFolder=None))


class FolderDetail(generics.RetrieveUpdateDestroyAPIView, FlexFieldsModelViewSet):
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Folder.objects.filter(Q(Owner=user))


class Register(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoggedInUserDetail(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)


class FileDownload(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        file = get_object_or_404(File, pk=kwargs['id'])
        file_handle = file.FileData.open()
        mimetype, _ = mimetypes.guess_type(file.FileData.path)
        response = FileResponse(file_handle, content_type=mimetype)
        response['Content-Length'] = file.FileData.size
        response['Content-Disposition'] = f"attachment; filename={file.Name.split('/')[-1:][0]}"
        return response


# TODO
@api_view(['GET'])
def TryToSendVerificationCode(request):
    email = request.query_params['email']

    # try_to_send_email(email)
    # if sent:
    return Response(data={'state': 'sent'})
    # else:
    # return Response(data={'state': 'failed'})
