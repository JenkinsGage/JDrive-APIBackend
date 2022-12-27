from django.urls import path
from . import views

urlpatterns = [
    path('files/', views.FileList.as_view()),
    path('folders/', views.FolderList.as_view()),
    path('users/', views.UserList.as_view()),
    path('files/<str:pk>/', views.FileDetail.as_view())
]
