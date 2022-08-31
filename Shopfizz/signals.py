from cProfile import Profile
from .models import Customer_Profile
from Users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save , sender=User)
def create_profile(sender , created , instance , **kwargs):
    if created and instance.is_seller==False:
        Customer_Profile.objects.create(customer=instance)
