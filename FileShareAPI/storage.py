import os
import hashlib
from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


def GetHashName(instance, filename):
    _, ext = os.path.splitext(filename)
    if instance.Hash is None:
        instance.FileData.open()
        contents = instance.FileData.read()

        sha256 = hashlib.sha256(contents).hexdigest()
    else:
        sha256 = instance.Hash
    return f'{sha256}{ext}'
