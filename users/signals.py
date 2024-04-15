from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings

# @receiver(post_save,sender=Profile)    
def createProfile(sender,instance,created,**kwags):
    if created:
        user=instance
        profile=Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject = 'welcome to devsearch'
        message = 'we are glad to see you here!'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )



def updateUser(sender,instance,created,**kwargs):
    Profile = instance
    user = Profile.user
    if created == False:
        user.first_name = Profile.name
        user.username = Profile.username
        user.email = Profile.email
        user.save()
           

def deleteUser(sender,instance,**kwags):
    user=instance.user
    user.delete()
    


post_save.connect(createProfile,sender=User)        
post_save.connect(updateUser,sender=Profile)        
post_delete.connect(deleteUser,sender=Profile)        