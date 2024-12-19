from django.contrib import admin
from .models import Client, User, Booking, Hostel, Room, RoomImage

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline]

# Register your models here.
admin.site.register(Client)
admin.site.register(Booking)
admin.site.register(Hostel)
admin.site.register(Room, RoomAdmin)

admin.site.register(RoomImage)
