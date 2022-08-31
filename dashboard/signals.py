from Users.models import User
from .models import Seller_Profile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save , sender=User)
def create_profile(sender , instance , created , **kwargs):

    if created and instance.is_seller==True:

        Seller_Profile.objects.create(seller=instance)


