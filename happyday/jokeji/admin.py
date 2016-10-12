from django.contrib import admin
from jokeji.models import *

# Register your models here.


class jokejiAdmin(admin.ModelAdmin):
    list_display = ('urlpath', 'title', 'joke',)

admin.site.register(jokeji, jokejiAdmin)
