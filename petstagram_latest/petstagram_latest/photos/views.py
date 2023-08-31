from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from petstagram_latest.photos.forms import PhotoCreateForm, PhotoEditForm, PhotoDeleteForm
from petstagram_latest.photos.models import Photo


def details_photo(request, pk):
    photo = Photo.objects.filter(pk=pk).get()
    user_liked_photos = Photo.objects.filter(pk=pk, user_id=request.user.pk)
    user = request.user

    context = {
        'photo': photo,
        'has_user_liked_photo': user_liked_photos,
        'likes_count': photo.photolike_set.count(),
        'is_owner': request.user == photo.user,
        'user': user,
    }
    return render(request, 'photos/photo-details-page.html', context)


def get_post_photo_form(request, form, success_url, template_path, pk=None):
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(success_url)

    context = {
        'form': form,
        'pk': pk,
    }

    return render(request, template_path, context)


@login_required
def add_photo(request):
    if request.method == 'GET':  # if request is GET
        form = PhotoCreateForm()
    else:
        # request.method == 'POST'
        form = PhotoCreateForm(request.POST, request.FILES)  # form is taken from user input
        if form.is_valid():                         # if the form is with valid user input
            photo = form.save(commit=False)         # save form and take it to use pk
            photo.user = request.user               # set current user as photo user
            photo.save()                            # save photo to db
            form.save_m2m()                         # save many-to-many relation to table

            return redirect('details photo', pk=photo.pk)

    context = {
        'form': form,
    }

    return render(request, 'photos/photo-add-page.html', context)


def edit_photo(request, pk):
    photo = Photo.objects.filter(pk=pk).get()
    return get_post_photo_form(
        request,
        PhotoEditForm(request.POST or None, instance=photo),
        success_url=reverse('index'),
        template_path='photos/photo-edit-page.html',
        pk=pk,
    )


def delete_photo(request, pk):
    photo = Photo.objects.filter(pk=pk).get()
    return get_post_photo_form(
        request,
        PhotoDeleteForm(request.POST or None, instance=photo),
        success_url=reverse('index'),
        template_path='photos/photo-delete-page.html',
        pk=pk,
    )
