# FROM Source - https://stackoverflow.com/a/24809190
# Posted by Gravity Grave, modified by community. See post 'Timeline' for change history
# Retrieved 2026-04-27, License - CC BY-SA 3.0

from allauth.account.signals import email_confirmation_sent, user_signed_up, email_confirmed
from django.dispatch import receiver
from allauth.account.models import EmailAddress

from .models import User

# @receiver(email_confirmation_sent, sender=EmailAddress)
# def user_signed_up_(request, email_address, **kwargs):

#     user = User.objects.get(email=email_address.email)
#     user.is_active = False

#     user.save()

from allauth.account.models import EmailConfirmationHMAC

@receiver(email_confirmation_sent, sender=EmailConfirmationHMAC)
def deactivate_on_confirmation_sent(request, confirmation, signup, **kwargs):
    if signup:  # only deactivate on signup, not on email change
        user = confirmation.email_address.user
        user.is_active = False
        user.save()



# FROM Source - https://stackoverflow.com/a/24817474
# Posted by Gravity Grave
# Retrieved 2026-04-27, License - CC BY-SA 3.0

@receiver(email_confirmed, sender=EmailAddress)
def email_confirmed_(request, email_address, **kwargs):

    user = User.objects.get(email=email_address.email)
    user.is_active = True

    user.save()

