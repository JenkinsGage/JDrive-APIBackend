import uuid
import hashlib

from django.db import models
from .storage import OverwriteStorage, GetHashName


class Item(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='Items')
    Name = models.CharField(default=None, max_length=256)
    Type = models.CharField(max_length=8, default=None)


class File(Item):
    UploadedTime = models.DateTimeField(auto_now=True)
    Hash = models.CharField(max_length=64, default=None)
    FileData = models.FileField(upload_to=GetHashName, storage=OverwriteStorage)
    ParentFolder = models.ForeignKey('Folder', on_delete=models.CASCADE, related_name='Files', blank=False, null=False)

    def save(self, *args, **kwargs):
        if self.Hash is None:
            data_bytes = self.FileData.read()
            self.Hash = hashlib.sha256(data_bytes).hexdigest()

        if self.Name is None:
            self.Name = self.FileData.name

        self.Type = 'File'
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        files_with_same_data = File.objects.filter(FileData=self.FileData)
        if files_with_same_data.count() == 1:
            self.FileData.delete()
            print(f'File {self.FileData} Was Permanently Removed From Disk')
        return super().delete(using, keep_parents)

    def __str__(self):
        return f'{self.FileData.name}({self.Id})'


class Folder(Item):
    CreatedTime = models.DateTimeField(auto_now=True)
    # Files = models.ManyToManyField(File, 'Folder', blank=True)
    ParentFolder = models.ForeignKey('self', on_delete=models.CASCADE, related_name='SubFolders', blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.Type = 'Folder'
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.Name}({self.Id})'
