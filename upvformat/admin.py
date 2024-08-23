from django.contrib import admin
from .models import UserProfile
from .models import Conversion


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
   list_display = ['user']
   raw_id_fields = ['user']

admin.site.register(Conversion)
