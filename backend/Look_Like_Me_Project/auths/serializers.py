from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from allauth.account.adapter import get_adapter

class CustomRegisterSerializer(RegisterSerializer):
    username = None  # Remove username field
    name = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'name': self.validated_data.get('name', ''),

        })
        return data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        user = adapter.save_user(request, user, self, commit=False)
        user.name = self.cleaned_data.get('name')
        user.save()

        # # Create profile with extra fields
        # user.profile.phone_number = self.cleaned_data.get('phone_number')
        # user.profile.company = self.cleaned_data.get('company')
        # user.profile.save()

        # self.custom_signup(request, user)
        return user