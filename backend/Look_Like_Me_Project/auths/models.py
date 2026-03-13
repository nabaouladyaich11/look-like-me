from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import FileExtensionValidator
from relations.models import Friendship


class User(AbstractBaseUser):
    """
    Extending AbstractBaseUser instead of Model because:
    - It provides built-in password hashing (never store plain text passwords)
    - It integrates with Django's auth system (sessions, permissions, decorators)
    - It gives us `last_login` tracking for free
    - AbstractBaseUser (vs AbstractUser) gives full control over required fields
    """
    name = models.CharField(max_length=200)

    email = models.EmailField(unique=True)
    # password field is inherited from AbstractBaseUser
    # AbstractBaseUser stores it hashed automatically via set_password()

    gender =models.CharField(
        max_length=6,
        choices=GenderChoices.choices)
    birth_date = models.DateField() # not datetime
    country = models.CharField(max_length=100)

    profile_photo = models.ImageField( # so Django validates it's a real image
        upload_to='profile_photos/', 
        null=True, 
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        # validators enforce allowed formats at app layer
        )
    bio = models.TextField(
        max_length=300,
        blank=True,
        default='',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    # set once on creation, never updated

    # friends = models.ManyToManyField(
    #     'self',
    #     through=Friendship,
    #     symmetrical=False,
    #     through_fields=('sender', 'receiver'),
    # ) CONSIDER: how to distingush friendship symmetry between 'pending and 'accepted'

    # Required by AbstractBaseUser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'gender', 'birth_date', 'country']

    class GenderChoices(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        

    def __str__(self):
        return self.name
