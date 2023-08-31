from django.contrib import admin
# TODO
from petstagram_latest.common.models import PhotoComment


@admin.register(PhotoComment)
class CommonAdmin(admin.ModelAdmin):
    pass
