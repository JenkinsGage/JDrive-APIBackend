from rest_framework import permissions
from django.db.models import Q
from .models import Share
from django.utils import timezone


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.Owner == request.user


class ShareAccessPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if 'Code' in request.query_params and request.query_params['Code'] == obj.Code:
            return True
        if obj.Code is (None or '') or obj.Members.contains(request.user) or request.user == obj.Owner:
            return True
        return False


class ItemPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Grant owner all the permission
        if obj.Owner == request.user:
            return True
        # Query all the valid shares
        queryset = Share.objects.filter(
            Q(Members=request.user) & (Q(OutdatedTime__gt=timezone.now()) | Q(OutdatedTime=None)) & Q(Items=obj))
        queryset_type1 = queryset.filter(ShareType=1)

        match request.method:
            case 'GET':
                if queryset.exists():
                    return True
            case 'DELETE':
                if obj.Type == 'Folder' and obj.Creator == request.user \
                        and len(obj.Files.all()) == 0 and queryset_type1.exists():
                    return True
                if obj.Type == 'File' and obj.Creator == request.user and queryset_type1.exists():
                    return True
            case 'PUT':
                if obj.Creator == request.user and queryset_type1.exists():
                    return True

        return False


class ShareAddItemPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if Share.objects.get(Id=view.kwargs['share']).Owner == request.user:
            return True

        queryset = Share.objects.filter(Q(Id=view.kwargs['share']) & Q(ShareType=1) & Q(Members=request.user)
                                        & (Q(OutdatedTime__gt=timezone.now()) | Q(OutdatedTime=None)))
        if queryset.exists():
            return True
