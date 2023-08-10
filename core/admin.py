from django.contrib import admin

# Register your models here.
from embed_video.admin import AdminVideoMixin
from .models import Item, Item2, Item3, Item4

class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(Item, MyModelAdmin)

admin.site.register(Item2, MyModelAdmin)

admin.site.register(Item3, MyModelAdmin)

admin.site.register(Item4, MyModelAdmin)