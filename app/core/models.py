from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                            PermissionsMixin
from django.conf import settings
from django.utils.html import format_html

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """ Create and save User """

        if not email:
            raise ValueError('User must have an email')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Creates and saves new superuser """
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that's supports email instead of username """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag for using recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Brand(models.Model):
    """ Implementing Brand model creation """

    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Promo(models.Model):
    """Implementing Promo model"""

    promo_type = models.CharField(max_length=128)
    description = models.TextField()
    end_time = models.DateField(null=True)

    def __str__(self):
        return self.promo_type


class Category(models.Model):
    """Implementing category model creation """

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Item(models.Model):
    """ Implementing Item model"""

    description = models.TextField()
    model = models.CharField(max_length=128)
    price = models.FloatField()
    color = models.CharField(max_length=30)
    warranty = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    brand_name = models.ForeignKey(Brand,
                                   on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE, default=None)
    promo = models.ManyToManyField(Promo)

    def __str__(self):
        return f'{self.brand_name} {self.model}'


class Notebook(Item):
    """Implementing Notebook model"""

    display = models.DecimalField(max_digits=5, decimal_places=4)
    memory = models.IntegerField()
    video_memory = models.IntegerField()
    cpu = models.CharField(max_length=150)


class Dishwasher(Item):
    """ Implementing Dishwasher model"""

    energy_saving_class = models.CharField(max_length=2, default="A+")
    power = models.IntegerField(default=0)
    width = models.FloatField()
    height = models.FloatField()

    def colored_name(self):
        return format_html(
            "<span style='color: #ff0000;'>{} {}</span>",
            self.model,
            self.brand_name
        )


class Ingredient(models.Model):
    """Ingredient to be used in Recipe"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
