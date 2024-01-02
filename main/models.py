from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
# Create your models here.





class category(models.Model):
       name        = models.CharField(max_length=50)
       slug        = models.SlugField(max_length=200, unique=True)
       description = models.TextField(max_length=300, blank=True)
       image       = models.ImageField(upload_to='photos/categories', blank=True)

       class Meta:
              verbose_name = 'category'
              verbose_name_plural = 'categories'
       
       def __str__(self):
              return self.name
       
       def get_url(self):
              return reverse('products_by_category', args=[self.slug])


class banner(models.Model):
       image = models.ImageField(upload_to='photos/Banner')


class Product(models.Model):
       name            = models.CharField(max_length=100, unique=True)
       slug            = models.CharField(max_length=150, unique=True)
       description     = models.TextField(max_length=500, blank=True)
       price           = models.IntegerField()
       image           = models.ImageField(upload_to='photos/products')
       stock           = models.IntegerField()
       is_available    = models.BooleanField(default=True)
       category        = models.ForeignKey(category, on_delete=models.CASCADE)
       created_date    = models.DateTimeField(auto_now_add=True)
       modified_date   = models.DateTimeField(auto_now=True)

       def __str__(self):
              return self.name
       
       def get_url(self):
              return reverse('product_detail', args=[self.category.slug, self.slug])


class MyAccountManager(BaseUserManager):
       def create_user(self, firstname, lastname, username, email, password=None):
              if not email:
                     raise ValueError('Email Address Required')
              if not username:
                     raise ValueError('Username Required')
             
              user = self.model(
                     email     = self.normalize_email(email),
                     username  = username,
                     firstname = firstname,
                     lastname  = lastname,
              )

              user.set_password(password)
              user.save(using=self._db)
              return user
       
       def create_superuser(self, firstname, lastname, email, username, password):
              user = self.create_user(
                     email     = self.normalize_email(email),
                     username  = username,
                     firstname = firstname,
                     lastname  = lastname,
                     password  = password,
              )

              user.is_admin      = True
              user.is_active     = True
              user.is_staff      = True
              user.is_superadmin = True

              user.save(using=self._db)
              return user


class Accounts(AbstractBaseUser):
       firstname    = models.CharField(max_length=50)
       lastname     = models.CharField(max_length=50)
       username     = models.CharField(max_length=50)
       email        = models.EmailField(max_length=100, unique=True)
       phone_number = models.CharField(max_length=50)

       # required
       date_joined   = models.DateTimeField(auto_now_add=True)
       last_login    = models.DateTimeField(auto_now_add=True)
       is_admin      = models.BooleanField(default=False)
       is_staff      = models.BooleanField(default=False)
       is_active     = models.BooleanField(default=False)
       is_superadmin = models.BooleanField(default=False)

       USERNAME_FIELD  = 'email'
       REQUIRED_FIELDS = ['username', 'firstname', 'lastname']

       objects = MyAccountManager()

       def __str__(self):
              return self.email
       
       def has_perm(self, perm, obj=None):
              return self.is_admin
       
       def has_module_perms(self, add_label):
              return True
       


class cart(models.Model):
       cart_id = models.CharField(max_length=250, blank=True)
       date_added = models.DateField(auto_now_add=True)

       def __str__(self):
              return self.cart_id



class VariationManager(models.Manager):
       def colors(self):
              return super(VariationManager, self).filter(variation_category='color', is_active=True)
       
       def sizes(self):
              return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
       ('color', 'color'),
       ('size','size'),
)


class variation(models.Model):
       product = models.ForeignKey(Product, on_delete=models.CASCADE)
       variation_category = models.CharField(max_length=100, choices=variation_category_choice)
       variation_value = models.CharField(max_length=100)
       is_active = models.BooleanField(default=True)
       created_date = models.DateTimeField(auto_now=True)
       objects = VariationManager()

       def __str__(self):
              return self.variation_value




class cartitem(models.Model):
       variations = models.ManyToManyField(variation, blank=True)
       product = models.ForeignKey(Product, on_delete=models.CASCADE)
       cart = models.ForeignKey(cart, on_delete=models.CASCADE)
       quantity = models.IntegerField()
       is_active = models.BooleanField(default=True)

       def sub_total(self):
              return self.product.price * self.quantity

       def __unicode__(self):
              return self.product 










