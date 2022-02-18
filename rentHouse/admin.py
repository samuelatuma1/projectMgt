from django.contrib import admin

# Register your models here.
from .models import House_Photos, UserProfile, Region, HouseType, State, UploadHouse

def change_status(modeladmin, request, queryset):
    for profile in queryset:
        profile.status = f"{profile.user.username} uses this app"
        profile.save()

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "status"]
    actions = [change_status]
    
admin.site.register(Region)
admin.site.register(HouseType)
admin.site.register(State)
admin.site.register(UploadHouse)

@admin.register(House_Photos)
class HousePhotosAdmin(admin.ModelAdmin):
    list_display = ['desc']
    

    
