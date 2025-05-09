from django.contrib import admin
from .models import Event, Note, Tag

admin.site.register(Event)
admin.site.register(Note)
admin.site.register(Tag)
