from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
import uuid

class UserProfile(models.Model):
    class Meta:
        db_table = "django_user_profile"

    field_names = ["bio", "company_name", "job"]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        auto_created=True
    )

    bio = models.CharField(max_length=512, null=True)

    company_name = models.CharField(max_length=512, null=True)

    job = models.CharField(max_length=512, null=True)

    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile',
        null=False
    )

    def upload_avatar_to(
        instance, filename): return "Avatar/{}.{}".format(uuid.uuid4(),filename)
    avatar = models.ImageField(
        gettext_lazy("avatar"),
        upload_to=upload_avatar_to,
        default="Avatar/default.png"
    )

    def to_json(self):
        # print(dir(self))
        # print(self.avatar.url)
        return {
            "id": self.id,
            "bio": self.bio,
            "company_name": self.company_name,
            "job": self.job,
            "company_name": self.company_name,
            "avatar": self.avatar.url
        }


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, full_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, full_name, password, **other_fields)

    def create_user(self, email, username, full_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(
            email=email, username=username,
            full_name=full_name,
            **other_fields
        )
        user.set_password(password)
        user.save()
        user_profille = UserProfile(user=user)
        user_profille.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = "django_user"
    #username, email, full_name, company_name
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False, auto_created=True
    )

    fields_name = ["email", "username", "full_name"]

    email = models.EmailField(gettext_lazy('email address'), unique=True)

    username = models.CharField(max_length=150, unique=True)

    full_name = models.CharField(max_length=150, unique=False)

    is_staff = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    company_name = models.CharField(max_length=150, unique=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.username

    def to_json(self):
        ...
        return {
            'id':self.id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'user_profile': self.user_profile.to_json()
        }