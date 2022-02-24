from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default= timezone.now)

    ## Creating foreign relationb with User table (one to many)....and CASCADE post on user deletion
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    ## Every time Post class runbs we get the following return statement as __str__ runs every time this class is called
    def __str__(self):

        return self.title

    def get_absolute_url(self):
        """
        This method is used to generate dynamic url. 
        It does it by using reverse method which takes url name and kwargs where the dynamic values are passed 
        which are expected in the url.
        
        """

        return reverse('post-detail', kwargs={'pk': self.pk})