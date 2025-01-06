from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from .models import Post
from django.contrib.auth.models import User
import os
import shutil

from .utils import get_random_code


@receiver(pre_save, sender=Post)
def pre_save_create_slug(sender, instance, **kwargs):
    if not instance.slug:
        # instance.slug = slugify(instance.author.username + " " + instance.title)
        instance.slug = slugify(instance.title + " " + get_random_code())
        
"""
slugify();
a = 'umit arat'
print(slugify(a)) ==> umit-arat
"""


@receiver(post_delete, sender=User)
def delete_user_directory(sender, instance, **kwargs):
    """
    Kullanıcı silindiğinde, kullanıcıya ait media/blog/{user_id}/ klasörünü siler.
    """
    user_directory = os.path.join('media', 'blog', str(instance.id))
    if os.path.exists(user_directory):
        shutil.rmtree(user_directory)  # Klasör ve içindekileri siler.
    