# from django.db import models
from . import models as db_models
from django.dispatch import receiver
from django.db.models.signals import (
    # pre_save,
    post_save
    # post_delete
)

# @receiver(pre_save)
# def delete_old_files_on_update(sender, instance, **kwargs):
#     if hasattr(instance, 'pk') and instance.pk:
#         try:
#             old_instance = sender.objects.get(pk=instance.pk)
#             for field in instance._meta.fields:
#                 if isinstance(field, models.ImageField) or isinstance(field, models.FileField):
#                     old_file = getattr(old_instance, field.name, None)
#                     new_file = getattr(instance, field.name, None)

#                     if old_file != new_file and old_file:
#                         old_file.delete(save=False)
#         except sender.DoesNotExist:
#             pass
#         except Exception as e:
#             print(f'Error in delete old files on update from S3: {e}')


@receiver(post_save, sender=db_models.SamajGallery)
def add_title(sender, instance, created, **kwargs):
    try:
        if not hasattr(instance, '_already_saved') and not instance.title:
            instance.title = f'Image {instance.pk}'
            instance._already_saved = True
            instance.save()
    except Exception as e:
        print(f'Error in add title post save signal: {e}')


# @receiver(post_delete)
# def delete_files_on_model_delete(sender, instance, **kwargs):
#     try:
#         for field in instance._meta.fields:
#             if isinstance(field, models.ImageField) or isinstance(field, models.FileField):
#                 file = getattr(instance, field.name, None)
#                 if file:
#                     file.delete(save=False)
#     except Exception as e:
#         print(f'Error in delete files on model delete: {e}')
