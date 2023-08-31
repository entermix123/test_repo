from django.contrib.auth import get_user_model
from django.db import models
# TODO
from petstagram_latest.photos.models import Photo

'''
Creating the Comment Model
It is time to create the comment model.
The field Comment Text is required:
• Comment Text - it should consist of a maximum of 300 characters
An additional field should be created:
• Date and Time of Publication - when a comment is created (only), the date of publication is automatically
generated
One more thing we should keep in mind is that the comment should relate to the photo (as in social apps users
comment on a specific photo/post, i.e., the comment object is always connected to the photo object).
'''

UserModel = get_user_model()


class PhotoComment(models.Model):
    MAX_TEXT_LENGTH = 300

    text = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        null=False,
        blank=False,
    )

    publication_date_and_time = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=True,
    )

    photo = models.ForeignKey(
        Photo,
        on_delete=models.RESTRICT,
        null=False,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )


class PhotoLike(models.Model):

    # Photo's field for likes is named {NAME_OF_THIS_MODEL.lower()}_set
    photo = models.ForeignKey(
        Photo,
        on_delete=models.RESTRICT,
        null=False,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )
