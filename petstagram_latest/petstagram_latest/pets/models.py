from django.contrib.auth import get_user_model

from core.model_mixins import StrFromFieldsMixin
from django.db import models
from django.utils.text import slugify

'''
Creating the Pet Model
Let us start by creating the Pet model.
The fields Name and Pet Photo are required:
• Name - it should consist of a maximum of 30 characters.
• Personal Pet Photo - the user can link a picture using a URL
The field date of birth is optional:
• Date of Birth - pet's day, month, and year of birth
Open the pets/models.py file and let us create the model:
'''

UserModel = get_user_model()


class Pet(StrFromFieldsMixin, models.Model):
    str_fields = ('name', 'id')

    NAME_MAX_LENGTH = 30

    # always set null=False first, after null=True and relations last 1-to-1, 1-to-many and many-to-many

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        null=False,
        blank=False,
    )

    personal_photo = models.URLField(
        null=False,
        blank=False,
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )

    def save(self, *args, **kwargs):

        # create id / update
        super().save(*args, **kwargs)                          # create id

        if not self.slug:                                      # add condition in django pipeline
            self.slug = slugify(f'{self.id}-{self.name}')      # if no slug, create one with id and name

        # Update
        return super().save(*args, **kwargs)                   # continue django code with save slug
