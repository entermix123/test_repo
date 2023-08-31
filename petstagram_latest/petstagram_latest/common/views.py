import pyperclip
from django.contrib.auth.decorators import login_required

from core.photo_utils import apply_likes_count, apply_user_liked_photo
from django.shortcuts import render, redirect
from django.urls import reverse

from petstagram_latest.common.forms import PhotoCommentForm, SearchPhotoForm
from petstagram_latest.common.models import PhotoLike
from petstagram_latest.common.utils import get_photo_url
from petstagram_latest.photos.models import Photo


def index(request):
    # TODO: fix this for current user when authentication is available
    search_form = SearchPhotoForm(request.GET)
    search_pattern = None
    if search_form.is_valid():
        search_pattern = search_form.cleaned_data['pet_name']

    photos = Photo.objects.all()

    if search_pattern:
        photos = photos.filter(tagged_pets__name__contains=search_pattern)

    # go true every photo and take likes
    photos = [apply_likes_count(photo) for photo in photos]
    photos = [apply_user_liked_photo(photo) for photo in photos]

    context = {
        'photos': photos,
        'comment_form': PhotoCommentForm(),
        'search_form': search_form,
    }
    return render(request, 'common/home-page.html', context)


@login_required
def like_photo(request, photo_id):
    # get users who liked the photo
    user_liked_photos = PhotoLike.objects.filter(photo_id=photo_id, user_id=request.user.pk)

    if user_liked_photos:                                       # if any users liked the photo
        PhotoLike.objects.filter(photo_id=photo_id).delete()    # remove a like
    else:
        # option 2
        PhotoLike.objects.create(                               # else add like to the photo
            photo_id=photo_id,
            user_id=request.user.pk,
        )

    return redirect(get_photo_url(request, photo_id))

    # # option 1
    # photo_like = PhotoLike(
    #     photo_id=photo_id,
    # )
    # photo_like.save()

    # # option 3 (wrong, additional call to DB)
    # # correct only if validation is needed
    # photo = Photo.objects.get(pk=photo_id)
    # photo_like.objects.create(
    #     photo=photo,
    # )


def share_photo(request, photo_id):
    photos_details_url = reverse(
        'details photo',
        kwargs={
            'pk': photo_id
        })
    pyperclip.copy(photos_details_url)
    return redirect(get_photo_url(request, photo_id))


@login_required
def comment_photo(request, photo_id):
    photo = Photo.objects.filter(pk=photo_id).get()

    form = PhotoCommentForm(request.POST)
    user = request.user

    if form.is_valid():
        comment = form.save(commit=False)       # commit=False does not persist to DB
        comment.photo = photo
        comment.user = user
        comment.save()

    return redirect('index')
