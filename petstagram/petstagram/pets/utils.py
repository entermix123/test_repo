from petstagram.pets.models import Pet


def get_pet_by_name_and_username(pet_slug, username):
    return Pet.objects.filter(slug=pet_slug, user__username=username).get()


def is_owner(request, obj):             # used for function-based views like function
    return request.user == obj.user


# # used for class-based views like mixin
# can be set to mixin and inherit of any class that need ownership
# class OwnerRequired:
#
#     def get(self, request, *args, **kwargs):
#         result = super().get(request, *args, *kwargs)
#
#         if request.user == self.object.user:
#             return result
#         else:
#             return '...'
#
#     def post(self): ...

