from django.contrib.auth import forms as auth_form, get_user_model

# always get user model with get_user_model(). If we import directly the created class, it is not abstract and can
# cause problems if something is changed!
# user model should only exist on two places:
#   1- when the class is created
#   2- in settings AUTH_USER_MODEL = 'xxxxx'
UserModel = get_user_model()


class UserCreateForm(auth_form.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email')
        field_classes = {'username': auth_form.UsernameField}


class UserEditForm(auth_form.UserChangeForm):
    class Meta:
        model = UserModel
        fields = '__all__'
        field_classes = {'username': auth_form.UsernameField}
