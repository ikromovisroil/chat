from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Role)
admin.site.register(Group)
admin.site.register(Science)
admin.site.register(User)
admin.site.register(UserGroup)
admin.site.register(UserScience)
admin.site.register(Chat)


