from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):

    ## For one to one relation with user table
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ## upload to dwefine place where file will stored
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):

        return f'{self.user.username} Profile'

    ## Overriding self method to add image resize feature
    def save(self,*args, **kwargs):
        ## Calling parent save
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)