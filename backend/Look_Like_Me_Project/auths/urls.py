from django.urls import include, path, re_path
from allauth.account.views import ConfirmEmailView

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
    path("", include("dj_rest_auth.urls")),
    re_path( # == Regex path
        "^registration/account-confirm-email/(?P<key>[-:\w]+)/$", # captures the trailing key part and names it 'key'
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path('registration/', include('dj_rest_auth.registration.urls'))
    # registration/      dj_rest_auth.registration.views.RegisterView    rest_register
    # registration/account-confirm-email/<key>/  django.views.generic.base.TemplateView  account_confirm_email
    # registration/account-email-verification-sent/      django.views.generic.base.TemplateView  account_email_verification_sent
    # registration/resend-email/ dj_rest_auth.registration.views.ResendEmailVerificationView     rest_resend_email
    # registration/verify-email/ dj_rest_auth.registration.views.VerifyEmailView rest_verify_email
    
]
