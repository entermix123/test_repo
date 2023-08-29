from django.contrib import admin
from petstagram.common.models import PhotoComment


@admin.register(PhotoComment)
class CommonAdmin(admin.ModelAdmin):
    pass
