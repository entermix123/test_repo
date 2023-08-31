from enum import Enum           # Enum is iterable class

# import auth models with name auth_models to avoid name collisions
from django.contrib.auth import models as auth_models
from django.core import validators                      # import validators
from django.db import models                            # import models

from core.model_mixins import ChoicesEnumMixin
# import custom validator for username when user is created
from petstagram_latest.common.validators import validate_only_letters

'''
• The first and last names of each user should have a 
    - minimum length of 2
    - maximum length of 30
    - must contain only alphabetical letters
    - email in the app must be unique.
• The gender is a choice field where the user can choose between "Male", "Female" and "Do not show" options:
'''
'''
naming the model:
- generic - AppUser, ApplicationUser ... 
- prefix with app name - PetstagramUser
'''


class Gender(ChoicesEnumMixin, Enum):         # make class for gender choices - Enum is iterable
    male = 'Male'
    female = 'Female'
    DoNotShow = 'Do not show'


class AppUser(auth_models.AbstractUser):    # inherit AbstractBaseUser and PermissionsMixin
    MIN_LENGTH_FIRST_NAME = 3
    MAX_LENGTH_FIRST_NAME = 30

    MIN_LENGTH_LAST_NAME = 3
    MAX_LENGTH_LAST_NAME = 30

    first_name = models.CharField(
        max_length=MAX_LENGTH_FIRST_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LENGTH_FIRST_NAME),
            validate_only_letters,
        )
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_LAST_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LENGTH_LAST_NAME),
            validate_only_letters,
        )
    )

    email = models.EmailField(
        unique=True,
    )

    gender = models.CharField(          # create gender choice field
        choices=Gender.choices(),       # set choices to class Gender with function to choose
        max_length=Gender.max_len(),    # set max len field as class Gender function max_len()
    )

    # If we want to login with username see E:\Cources\Python Web Framework -
    # ноември 2022\3. User and Password Management\user management model
    # USERNAME_FIELD = 'email'  # change login to be with email (username will stay with no use if this is active)
