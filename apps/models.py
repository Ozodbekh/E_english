from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.models import ContentType
from django.db.models import PositiveSmallIntegerField, TextChoices, CharField, EmailField


class CostumeUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class UserRole(TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    email = EmailField("email address", unique=True, blank=True)
    objects = CostumeUserManager()
    rank = PositiveSmallIntegerField(default=0)
    role = CharField(max_length=50, choices=UserRole.choices, default=UserRole.USER)
