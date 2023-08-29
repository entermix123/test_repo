# mixin for disabling fields in classes
class DisableFormMixin:
    disabled_fields = ()        # create empty tuple for disabled fields
    fields = {}                 # creat dictionary for all instance fields in current action

    def _disable_fields(self):  # create protected disabled fields function for edit/delete page
        if self.disabled_fields == '__all__':   # if any fields are used add to tuple
            fields = self.fields.keys()         # take keys from dictionary
        else:
            fields = self.disabled_fields       # set all that exist

        for field_name in fields:                               # iterate true current fields
            if field_name in self.fields:                       # name of the field in used fields
                field = self.fields[field_name]                 # set current field
                # field.widget.attrs['disabled'] = 'disabled'     # set parameter to disabled
                field.widget.attrs['readonly'] = 'readonly'     # set parameter to read only
