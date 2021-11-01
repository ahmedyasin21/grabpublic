from django.contrib import admin
from .models import UserProfile,Rank

class NameingAdmin(admin.ModelAdmin):
    

    class Meta:
        model = UserProfile

admin.site.register(UserProfile,NameingAdmin)
admin.site.register(Rank)
# Register your models here.
