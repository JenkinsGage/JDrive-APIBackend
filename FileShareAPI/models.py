import uuid
import hashlib

from django.db import models
from .storage import OverwriteStorage, GetHashName


class Item(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='Items')
    Name = models.TextField(default=None)
    Access = models.ManyToManyField('auth.User', 'AccessibleItems')


class File(Item):
    UploadedTime = models.DateTimeField(auto_now=True)
    Hash = models.CharField(max_length=64, default=None)
    FileData = models.FileField(upload_to=GetHashName, storage=OverwriteStorage)

    class Meta:
        verbose_name = 'File'

    def save(self, *args, **kwargs):
        if self.Hash is None:
            data_bytes = self.FileData.read()
            self.Hash = hashlib.sha256(data_bytes).hexdigest()

        if self.Name is None:
            self.Name = self.FileData.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.FileData.name}({self.Id})'


class Folder(Item):
    CreatedTime = models.DateTimeField(auto_now=True)
    Files = models.ManyToManyField(File, 'Folders')
    ParentFolder = models.ForeignKey('self', on_delete=models.CASCADE, related_name='SubFolders', blank=True, null=True)

    class Meta:
        verbose_name = 'Folder'

    def __str__(self):
        return f'{self.Name}({self.Id})'
