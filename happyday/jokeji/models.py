from django.db import models

# Create your models here.


class jokeji(models.Model):
    urlpath = models.CharField(max_length=70)
    title = models.CharField(max_length=50)
    joke = models.TextField()

    # def __str__(self):
    #     return self.title
