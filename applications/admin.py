from django.contrib import admin
from .models import Stage, Application, Note, Attachment

admin.site.register(Stage)
admin.site.register(Application)
admin.site.register(Note)
admin.site.register(Attachment)
