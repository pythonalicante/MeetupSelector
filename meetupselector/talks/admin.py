from django.contrib import admin

from .models import Speaker, Talk, Topic

# Register your models here.
admin.site.register(Speaker)
admin.site.register(Topic)
admin.site.register(Talk)
