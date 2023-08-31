from django.contrib import admin
# TODO
from petstagram_latest.pets.models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    pass

