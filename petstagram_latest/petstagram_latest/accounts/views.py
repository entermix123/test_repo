from django.urls import reverse_lazy
from django.views import generic as views  # import generic with name views
# import views as _auth_views to avoid name collisions
from django.contrib.auth import views as auth_views, get_user_model

from petstagram_latest.accounts.forms import UserCreateForm

# always get user model with get_user_model(). If we import directly the created class, it is not abstract and can
# cause problems if something is changed!
# user model should only exist on two places:
#   1- when the class is created
#   2- in settings AUTH_USER_MODEL = 'xxxxx'
UserModel = get_user_model()


# def register_user(request):
#     return render(request, 'accounts/register-page.html')
class SignUpView(views.CreateView):
    template_name = 'accounts/register-page.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('index')


# def login_user(request):
#     return render(request, 'accounts/login-page.html')
class SignInView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')


# def details_user(request, pk):
#     return render(request, 'accounts/profile-details-page.html')
class UserDetailsView(views.DetailView):
    template_name = 'accounts/profile-details-page.html'
    model = UserModel

    def get_context_data(self, **kwargs):  # extend the context of the build in view
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.request.user == self.object
        context['pets_count'] = self.object.pet_set.count()

        # take objects with foreign key to this object
        # important N + 1 query problem !!!
        # prefetch_related('photolike_set') - Return a new QuerySet in Many-To-One and Many-To-Many related likes
        # select_related('user') - Return a ONE new QuerySet instance that will select related users.

        photos = self.object.photo_set.prefetch_related('photolike_set')
        # photos = self.object.photo_set.select_related('user')

        pet_photos = self.object.photo_set.select_related('user')
        if pet_photos:
            last_pet_photo_pk = max([x.pk for x in pet_photos])
            last_photo = [x for x in pet_photos if x.pk == last_pet_photo_pk][0]

            context['last_pet_photo'] = last_photo
        context['photos_count'] = photos.count()
        context['likes_count'] = sum(x.photolike_set.count() for x in photos)

        return context


# def edit_user(request, pk):
#     return render(request, 'accounts/profile-edit-page.html')
class UserEditView(views.UpdateView):
    template_name = 'accounts/profile-edit-page.html'
    model = UserModel
    fields = ('first_name', 'last_name', 'email', 'gender',)

    def get_success_url(self):
        return reverse_lazy('user details', kwargs={
            'pk': self.request.user.pk,
        })


# def delete_user(request, pk):
#     return render(request, 'accounts/profile-delete-page.html')
class UserDeleteView(views.DeleteView):
    template_name = 'accounts/profile-delete-page.html'
    model = UserModel
    success_url = reverse_lazy('index')


'''
superuser:
username: daniomaster
pass: danio@123

user: Danio123
pass: dandan@123

user: daniodanio
pass: DanDan@123

user: dangedange
pass: Dangeto@123
'''
