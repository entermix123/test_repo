from django import forms

from core.form_mixins import DisableFormMixin
from petstagram.pets.models import Pet


# 'ModelForm' and 'Form'
# - 'ModelForm' bind to models
# - 'Form' is detached from models


class PetBaseForm(forms.ModelForm):

    # second option to add shadow text in required fields in the form true changing current widget
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['name'].widgets.attrs['placeholder'] = 'Pet name'

    class Meta:
        model = Pet
        # field = '__all__' ( we want to skip 'slug' )

        # take all required fields except slug (slug is automatically added) - option 1:
        fields = ('name', 'date_of_birth', 'personal_photo')

        # exclude slug and take the rest - option 2:
        # exclude = ('slug',)
        labels = {  # specify name of the field
            'name': 'Pet Name',
            'personal_photo': 'Link to Image',
            'date_of_birth': 'Date of Birth',
        }

        widgets = {  # make shadow text in the fields true overwrite widgets
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Pet name',
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'placeholder': 'mm/dd/yyyy',
                    # make action calendar appear and choose option
                    'type': 'date',
                }
            ),
            'personal_photo': forms.URLInput(
                attrs={
                    'placeholder': 'Link to Image',
                }
            ),
        }


class PetCreateForm(PetBaseForm):
    pass


class PetEditForm(DisableFormMixin, PetBaseForm):
    disabled_fields = ('name',)                 # disable name field when edit

    def __init__(self, *args, **kwargs):        # take instance init
        super().__init__(*args, **kwargs)       # inherit object data
        self._disable_fields()                  # add disabled fields


class PetDeleteForm(DisableFormMixin, PetBaseForm):
    disabled_fields = ('name', 'date_of_birth', 'personal_photo')       # disable fields when delete

    def __init__(self, *args, **kwargs):        # take instance init
        super().__init__(*args, **kwargs)       # inherit object data
        self._disable_fields()                  # add disabled fields

    def save(self, commit=True):                # overwrite save function when delete
        if commit:                              # if delete button is triggered
            self.instance.delete()              # delete instance
        else:
            pass
        return self.instance                    # return instance
