from django.contrib import admin

from meetupselector.talks.models import Talk, Topic

# Register your models here.
admin.site.register(Topic)
admin.site.register(Talk)
