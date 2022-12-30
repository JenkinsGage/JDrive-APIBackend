from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import permissions, generics
from rest_flex_fields import FlexFieldsModelViewSet, is_expanded
from .serializers import UserSerializer, FolderSerializer, FileSerializer, ItemSerializer
from .models import File, Folder, Item
from .permissions import IsOwnerOrAccessReadOnly


class ItemList(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Item.objects.filter(Owner=user)


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
        return File.objects.filter(Q(Owner=user) | Q(IsSharable=True) | Q(Access__in=[user]))


class FolderList(generics.ListCreateAPIView):
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Folder.objects.filter(Q(Owner=user) | Q(Access__in=[user]) | Q(IsSharable=True))

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
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAccessReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Folder.objects.filter(Q(Owner=user) | Q(Access__in=[user]) | Q(IsSharable=True))


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class LoggedInUserDetail(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)
