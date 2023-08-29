from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from core.photo_utils import apply_likes_count, apply_user_liked_photo
from django.shortcuts import render, redirect

from petstagram.pets.forms import PetCreateForm, PetEditForm, PetDeleteForm
from petstagram.pets.utils import get_pet_by_name_and_username, is_owner

UserModel = get_user_model()


def details_pet(request, username, pet_slug):           # need additional username and pet name parameters
    pet = get_pet_by_name_and_username(pet_slug, username)
    photos = [apply_likes_count(photo) for photo in pet.photo_set.all()]
    photos = [apply_user_liked_photo(photo) for photo in photos]

    context = {
        'pet': pet,
        'photos_count': pet.photo_set.count(),
        'pet_photos': photos,
    }
    return render(request, 'pets/pet-details-page.html', context)


@login_required
def add_pet(request):
    if request.method == 'GET':             # if request is GET
        form = PetCreateForm()
    else:
        # request.method == 'POST'              # if request is POST
        form = PetCreateForm(request.POST)      # form is taken from user input
        if form.is_valid():                     # if the form is with valid user input
            pet = form.save(commit=False)	    # set pet var
            pet.user = request.user		        # set current user
            pet.save()				            # save pat to db
            return redirect('user details', pk=request.user.pk)

    context = {
        'form': form,
    }

    return render(request, 'pets/pet-add-page.html', context)


def edit_pet(request, username, pet_slug):              # need additional username and pet name parameters
    pet = get_pet_by_name_and_username(pet_slug, username)

    if not is_owner:
        return redirect('details pet', username=username, pet_slug=pet_slug)  # require ownership to edit pet

    if request.method == 'GET':             # if request is GET
        form = PetEditForm(instance=pet)
    else:
        # request.method == 'POST'              # if request is POST
        form = PetEditForm(request.POST, instance=pet)      # form is taken from user input
        if form.is_valid():                                 # if the form is with valid user input
            form.save()                                     # save form
            return redirect('details pet', username=username, pet_slug=pet_slug)

    context = {
        'form': form,
        'pet_slug': pet_slug,
        'username': username,
        'is_owner': pet.user == request.user
    }
    return render(request, 'pets/pet-edit-page.html', context)


def delete_pet(request, username, pet_slug):            # need additional username and pet name parameters
    pet = get_pet_by_name_and_username(pet_slug, username)

    if request.method == 'GET':             # if request is GET
        form = PetDeleteForm(instance=pet)
    else:
        # request.method == 'POST'              # if request is POST
        form = PetDeleteForm(request.POST, instance=pet)      # form is taken from user input
        if form.is_valid():                                 # if the form is with valid user input
            form.save()                                     # save form
            return redirect('user details', pk=1)
    context = {
        'form': form,
        'pet_slug': pet_slug,
        'username': username,
    }

    return render(request, 'pets/pet-delete-page.html', context)
