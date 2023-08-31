from django import forms

from core.form_mixins import DisableFormMixin
from petstagram_latest.common.models import PhotoLike, PhotoComment
# TODO
from petstagram_latest.photos.models import Photo


class BasePhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('publication_date', 'user')


class PhotoCreateForm(BasePhotoForm):
    pass


class PhotoEditForm(BasePhotoForm):
    class Meta:
        model = Photo
        exclude = ('publication_date', 'photo')


class PhotoDeleteForm(DisableFormMixin, BasePhotoForm):
    disabled_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):        # overwrite save() method when delete photo

        if commit:
            self.instance.tagged_pets.clear()       # clear all tagged pets many-to-many connection

            # clear all tagged pates from the photo one-to-many connection
            Photo.objects.all().first().tagged_pets.clear()

            # clear all likes from the photo one-to-many connection
            PhotoLike.objects.filter(photo_id=self.instance.id).delete()

            # clear all comments from the photo one-to-many connection
            PhotoComment.objects.filter(photo_id=self.instance.id).delete()

            self.instance.delete()                  # delete the photo

        return self.instance
