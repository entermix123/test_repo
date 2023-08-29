from django.contrib.auth import get_user_model

from core.model_mixins import StrFromFieldsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from petstagram.pets.models import Pet
from petstagram.photos.validators import validate_file_less_than_5mb

'''
The field Photo is required:
• Photo - the user can upload a picture from storage, the maximum size of the photo can be 5MB
The fields description and tagged pets are optional:
• Description - a user can write any description of the photo; it should consist of a maximum of 300 characters
and a minimum of 10 characters
• Location - it should consist of a maximum of 30 characters
• Tagged Pets - the user can tag none, one, or many of all pets. There is no limit on the number of tagged pets
There should be created one more field that will be automatically generated:
• Date of publication - when a picture is added or edited, the date of publication is automatically generated
'''

UserModel = get_user_model()


class Photo(StrFromFieldsMixin, models.Model):
    str_fields = ('pk', 'photo', 'location')

    MIN_DESCRIPTION_LENGTH = 10     # POSTGRES DO NOT SUPPORT MIN CONDITION
    MAX_DESCRIPTION_LENGTH = 300

    MAX_LOCATION_LENGTH = 30

    # always set null=False first, after null=True and relations last:

    # 1-to-1 relations

    # 1-to-many relations

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )

    # many-to-many relations

    # require media files to work correctly
    photo = models.ImageField(
        upload_to='pet_photos/',     # create directory to save uploaded images
        null=False,                             # save every uploaded image but in DB saves only last one
        blank=True,
        validators=(validate_file_less_than_5mb,),
    )

    description = models.CharField(

        # DB validation
        max_length=MAX_DESCRIPTION_LENGTH,

        validators=(
            # Django validation, not DB validation
            MinLengthValidator(MIN_DESCRIPTION_LENGTH),
        ),
        null=True,
        blank=True,
    )

    location = models.CharField(
        max_length=MAX_LOCATION_LENGTH,
        null=True,
        blank=True,
    )

    publication_date = models.DateTimeField(
        auto_now=True,  # automatically sets current date on 'save' (create or update)
        # auto_now_add=True,        # ser current date on creation only, not save or update
        null=False,
        blank=True,
    )

    tagged_pets = models.ManyToManyField(
        Pet,           # example that created apps should be nested, if not nested depends on one app
        blank=True,
    )
