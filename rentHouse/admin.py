from django.contrib import admin

# Register your models here.
from .models import UserProfile

def change_status(modeladmin, request, queryset):
    for profile in queryset:
        profile.status = f"{profile.user.username} uses this app"
        profile.save()

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "status"]
    actions = [change_status]
    
