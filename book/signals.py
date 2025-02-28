from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from book.models import Book


@receiver([post_save, post_delete], sender=Book)
def invalidate_cache(sender, instance, **kwargs):
    cache.delete_pattern("*book_view*")
    cache.delete_pattern("*borrowing_view*")
