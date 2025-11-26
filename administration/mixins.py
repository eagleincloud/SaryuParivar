from django.db import models

class FileDeleteMixin:
    """
    Mixin that deletes files from ImageField or FileField on model update or delete.
    """

    def delete_files(self):
        """
        Deletes files stored in ImageField or FileField for this model instance.
        """
        for field in self._meta.fields:
            if isinstance(field, models.ImageField) or isinstance(field, models.FileField):
                file = getattr(self, field.name, None)
                if file:
                    file.delete(save=False)

    def save(self, *args, **kwargs):
        """
        Override save to delete old files when updating the object.
        """
        if self.pk:  # If it's an update (not a new object)
            # Get the old instance before the update
            old_instance = self.__class__.objects.get(pk=self.pk)
            
            # Compare old and new files and delete the old ones if the files have changed
            for field in self._meta.fields:
                if isinstance(field, models.ImageField) or isinstance(field, models.FileField):
                    old_file = getattr(old_instance, field.name, None)
                    new_file = getattr(self, field.name, None)
                    if old_file != new_file and old_file:
                        old_file.delete(save=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Override delete to remove files from storage when the object is deleted.
        """
        self.delete_files()  # Delete files from storage before deleting the model instance
        super().delete(*args, **kwargs)
