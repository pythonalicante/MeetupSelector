from django.contrib import admin

from meetupselector.proposals.models import Event, Proposal

admin.site.register(Proposal)
admin.site.register(Event)
