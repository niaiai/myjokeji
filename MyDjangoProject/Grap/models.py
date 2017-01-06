from django.db import models
# Create your models here.


class grap(models.Model):
    title = models.CharField(max_length=50)
    urlpath = models.CharField(max_length=70)
    click = models.IntegerField(default=1)
    update = models.DateTimeField()

    def __str__(self):
        return self.tittle


class img(models.Model):
    grap = models.ForeignKey(grap)
    title = models.CharField(max_length=50)
    path = models.CharField(max_length=70)
