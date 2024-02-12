#from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import uuid
from .utils import hash_token

class CustomUserManager(models.Manager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        if not password:
            raise ValueError('The Password field must be set')
        

        passw = hash_token(password)

        user = self.model(email=email, username=username, password=passw, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        return self.create_user( email, username, password, **extra_fields)

class User(models.Model):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        # Add more roles here
    )

    userID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=500, null=False, blank=False)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')
    isVerified = models.BooleanField(default=False)
    verifiedAt = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'email', 'password']

    def __str__(self):
        return self.userID, self.email

class Token(models.Model):
    userID = models.ForeignKey(User, related_name='tokens', on_delete=models.CASCADE, null=False, blank=False)
    token = models.CharField(max_length=500, null=False, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.userID, self.token

class Category(models.Model):
    categoryID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Item(models.Model):
    itemID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    SKU = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    tags = models.JSONField(blank=True, null=True, default=list)
    category = models.CharField(max_length=100, null=True, blank=True)
    units = models.CharField(max_length=100)
    minimum_stock = models.IntegerField()
    desired_stock = models.IntegerField()
    in_stock = models.IntegerField()
    available_stock = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('name',)


    def __str__(self):
        return self.itemID