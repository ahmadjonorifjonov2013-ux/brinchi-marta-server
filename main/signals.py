from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import HeaderMenu, HeroSection, ServiceItem, Testimonial

ALL_DATA_CACHE_KEY = "landing:all_data"


@receiver(post_save, sender=HeaderMenu)
@receiver(post_delete, sender=HeaderMenu)
@receiver(post_save, sender=HeroSection)
@receiver(post_delete, sender=HeroSection)
@receiver(post_save, sender=ServiceItem)
@receiver(post_delete, sender=ServiceItem)
@receiver(post_save, sender=Testimonial)
@receiver(post_delete, sender=Testimonial)
def clear_all_data_cache(sender, instance, **kwargs):
    cache.delete(ALL_DATA_CACHE_KEY)