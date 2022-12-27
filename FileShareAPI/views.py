from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, generics
from .serializers import UserSerializer, FolderSerializer, FileSerializer
from .models import File, Folder
from .permissions import IsUser, IsAdminOrOwner, IsAdminOrReadOnly, IsOwnerOrReadOnly


class FileList(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(Owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(Owner=user)


class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAdminOrOwner]


class FolderList(generics.ListCreateAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]

    def perform_create(self, serializer):
        serializer.save(Owner=self.request.user)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
