from django.urls import path, include
from petstagram_latest.accounts.views import SignInView, SignUpView, SignOutView, \
    UserDetailsView, UserEditView, UserDeleteView

urlpatterns = (
    path('register/', SignUpView.as_view(), name='register user'),
    path('login/', SignInView.as_view(), name='login user'),
    path('logout/', SignOutView.as_view(), name='logout user'),
    path('profile/<int:pk>/', include([
        path('', UserDetailsView.as_view(), name='user details'),
        path('edit/', UserEditView.as_view(), name='edit user'),
        path('delete/', UserDeleteView.as_view(), name='delete user'),
    ])),
)
