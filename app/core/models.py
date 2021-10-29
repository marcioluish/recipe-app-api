from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        # SELF.MODEL access the model which is being managed.
        # (cont) This is setup by BaseUserManager.
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # We use UserManager() to manage objects for the User Model.
    # (cont) It's accessed by User.objects, so that the manager
    # (cont) can be aware of the model it is managing.
    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    """
    Generally speaking, it’s easiest to refer to the user model with the
    "AUTH_USER_MODEL" setting in code that’s executed at import time, however,
    it’s also possible to call "get_user_model()" while Django is importing
    models, so you could use "models.ForeignKey(get_user_model(), ...)".
    As the models are executed at import time, it's somehow easier (or maybe
    even faster) to use AUTH_USER_MODEL notation than using
    models.ForeignKey(get_user_model(), ...). But both of them works.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # This insures that whenever a user is deleted, all recipes related
        # (cont) to they are deleted as well.
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    time_minutes = models.IntegerField()
    # 'blank=True' sets the 'link' field automatically to a blank string
    # when it's not provided by the user. Doing this, if we wanna check
    # if the link is set, we'd only check if it's blank or not, not needing
    # to check if it's 'Null/None'.
    link = models.CharField(max_length=255, blank=True)
    ingrediets = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
