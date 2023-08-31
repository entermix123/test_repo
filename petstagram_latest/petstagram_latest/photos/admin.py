from django.contrib import admin
from petstagram_latest.photos.models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'publication_date', 'pets')

    @staticmethod
    def pets(obj):
        tagged_pets = obj.tagged_pets.all()
        if tagged_pets:
            return ', '.join(p.name for p in tagged_pets)

        return 'No tagged pets'
