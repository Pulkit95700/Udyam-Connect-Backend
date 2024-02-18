from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# from django.core.validators import MaxLengthValidator

# Customer User manager
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, date of
        birth and password.
        """
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            username = username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User model
class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, verbose_name="Company Username")
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager() 

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password", ]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

# Adding a foreign key to store user profile

class Company(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="company")
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    company_name = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=200)
    gst_no = models.CharField(max_length=15)
    type = models.CharField(max_length=100, choices=[("regular", "Regular"), ("supplier", "Supplier")], default="regular")
    contact = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    constitution = models.CharField(max_length=100, choices=[("proprietorship", "Proprietorship"), ("partnership", "Partnership"), ("llp", "LLP"), ("pvt_ltd", "Pvt Ltd"), ("public_ltd", "Public Ltd")], default="proprietorship")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
     return self.company_name
