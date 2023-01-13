from django.contrib import admin
from .models import File, Folder, Share

admin.site.register(File)
admin.site.register(Folder)
admin.site.register(Share)
