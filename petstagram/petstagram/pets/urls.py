from django.urls import path, include
from petstagram.pets.views import add_pet, delete_pet, edit_pet, details_pet

urlpatterns = (
    path('add/', add_pet, name='add pet'),
    path('<str:username>/pet/<slug:pet_slug>/', include([       # slug is like primary key but string of pet name
        path('', details_pet, name='details pet'),
        path('edit/', edit_pet, name='edit pet'),
        path('delete/', delete_pet, name='delete pet'),
    ])),
)
