from datetime import timedelta

from ckeditor.fields import RichTextField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, IntegerField, PositiveIntegerField, TextChoices, ForeignKey, JSONField, \
    BooleanField, TextField
from django.db.models import SET_NULL, DecimalField
from django.utils.timezone import now
from django_resized import ResizedImageField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from apps.tasks import send_new_product_notification


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def created_at_product(self):
        return self.created_at.strftime("%d.%m.%Y")

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, email, password, **extra_fields)


class User(AbstractUser):
    class Type(TextChoices):
        ADMIN = "admin", "Admin"
        CURRIER = "currier", "Yetkazib beruvchi"
        USERS = "users", "Foydalanuvchi"
        OPERATOR = "operator", "Operator"
        MANAGER = "manager", "Menejer"

    type = CharField(max_length=25, choices=Type.choices, default=Type.USERS)
    intro = TextField(max_length=1024,null=True,blank=True)
    avatar = ResizedImageField(size=[168, 168], upload_to='user_avatars/', null=True, blank=True, default='user_avatars/avatar_default.jpeg')
    banner = ResizedImageField(size=[1198, 124], upload_to='user_banners/', null=True, blank=True, default='user_avatars/banner_default.jpg')
    workout = CharField(max_length=50)
    country = CharField(max_length=30)
    is_verified = BooleanField(default=False)
    phone_number = CharField(max_length=25)
    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class Category(MPTTModel):
    name = CharField(max_length=25)
    parent = TreeForeignKey('self', SET_NULL, 'category', null=True, blank=True)

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = CharField(max_length=255)
    description = RichTextField()
    price = DecimalField(max_digits=9, decimal_places=2)
    discount = IntegerField(default=0)
    specifications = JSONField()
    shipping = DecimalField(max_digits=9, decimal_places=2)
    quantity = PositiveIntegerField(default=0)
    category = models.ForeignKey('apps.Category', models.CASCADE, 'categories')

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        users_emails = list(User.objects.values_list('email', flat=True))
        send_new_product_notification.delay(users_emails, self.name, 'https://www.youtube.com/', )

    @property
    def stock(self):
        if self.quantity > 0:
            return "Available"
        else:
            return "Sold-out"

    def __str__(self):
        return self.name

    @property
    def is_new(self):
        return self.created_at >= now() - timedelta(days=7)

    @property
    def discount_price(self):
        return self.discount * self.price / 100

    @property
    def sell_price(self):
        return self.price - self.discount_price


class ProductImage(models.Model):
    image = ResizedImageField(size=[1098, 717], upload_to='product_images/', null=True, blank=True)
    product = models.ForeignKey('apps.Product', models.CASCADE, related_name='images')

    def __repr__(self):
        return self.product.name


class WishList(models.Model):
    user = ForeignKey('apps.User', on_delete=models.CASCADE, related_name='wishlists')
    product = ForeignKey('apps.Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    product = models.ForeignKey('apps.Product', models.CASCADE)
