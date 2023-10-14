from django.contrib import admin
from .models import Clients, Filterwords, Notifications, Sites, Articles
# Register your models here.
admin.site.register(Clients)
admin.site.register(Filterwords)
admin.site.register(Notifications)
admin.site.register(Sites)
admin.site.register(Articles)

