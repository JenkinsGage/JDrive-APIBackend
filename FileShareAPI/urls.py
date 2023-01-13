from django.urls import path
from . import views

urlpatterns = [
    # GET files/ - To get all the files the user owned
    # POST files/ - To upload and create a new file to the server
    path('files/', views.FileList.as_view()),

    # GET folders/ - To get all the folders the user owned
    # POST folders/ - To create a new folder
    path('folders/', views.FolderList.as_view()),

    # POST user/register/ - To register a new user
    path('user/register/', views.Register.as_view()),

    # GET hash/ - To get the files with the same hash
    path('hash/', views.FileByHash.as_view()),

    # GET files/<str:pk>/ - To get the file detail info of a given id
    # PUT files/<str:pk>/ - To modify the file with given id
    # DELETE files/<str:pk>/ - To delete the file with given id
    path('files/<str:pk>/', views.FileDetail.as_view()),

    # GET folders/<str:pk>/ - To get the folder detail info of a given id
    # PUT folders/<str:pk>/ - To modify the folder with given id
    # DELETE folders/<str:pk>/ - To delete the folder with given id
    path('folders/<str:pk>/', views.FolderDetail.as_view({'get': 'retrieve'})),

    # GET user/info/ - To get the basic info of user
    path('user/info/', views.LoggedInUserDetail.as_view()),

    # GET root/ - To get the root folder info of user
    path('root/', views.FolderRoot.as_view({'get': 'list'})),

    # GET download/<str:id>/ - To download the file with a given id
    path('download/<str:id>/', views.FileDownload.as_view()),

    path('shares/', views.ShareList.as_view()),

    path('shares/<str:pk>/', views.ShareDetail.as_view()),

    path('shares/<str:share>/create-folder/', views.CreateFolderViaShare.as_view())

    # TODO
    # GET verify/?email=xxxx@gmail.com
    # path('verify/', views.TryToSendVerificationCode)
]
