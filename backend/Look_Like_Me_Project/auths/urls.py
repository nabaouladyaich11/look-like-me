from django.urls import include, path, re_path
from allauth.account.views import ConfirmEmailView
from .views import LoginView, LogoutView, LogoutAllView, ManageUserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', LogoutAllView.as_view(), name='knox_logoutall'),

    # path("", include("knox.urls")),
    re_path( # == Regex path
        "^registration/account-confirm-email/(?P<key>[-:\w]+)/$", # captures the trailing key part and names it 'key'
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),

    path('registration/', include('dj_rest_auth.registration.urls')),

    path('profile/', ManageUserView.as_view(), name='user_profile'),

    
]
