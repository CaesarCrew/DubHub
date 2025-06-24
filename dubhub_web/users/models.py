from django.db import models
from django.utils.timezone import now
from core.consts import USER_TYPES
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        last_login = now()
        user = self.model(email=email, last_login=last_login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.user_type = 4
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=130, blank=True, null=True)
    user_type = models.SmallIntegerField(choices=USER_TYPES, verbose_name='type', default=0)
    photo = models.ImageField(upload_to='users/fotos', verbose_name='Foto', default=None, null=True, blank=True)

    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'first_name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email