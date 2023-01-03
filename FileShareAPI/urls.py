from django.urls import path
from . import views

urlpatterns = [
    path('files/', views.FileList.as_view()),
    path('folders/', views.FolderList.as_view()),
    path('users/', views.UserList.as_view()),
    path('hash/', views.FileByHash.as_view()),
    path('files/<str:pk>/', views.FileDetail.as_view()),
    path('folders/<str:pk>/', views.FolderDetail.as_view({'get': 'retrieve'})),
    path('user/info/', views.LoggedInUserDetail.as_view()),
    path('items/', views.ItemList.as_view()),
    path('root/', views.FolderRoot.as_view({'get': 'list'})),
    path('download/<str:id>/', views.FileDownload.as_view())
]
