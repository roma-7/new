from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Profile(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True,
                                           validators=[MinValueValidator(18), MaxValueValidator(100)])
    phone_number = models.PositiveIntegerField(null=True, blank=True)

    STATUS_USER = (
        ('золото', 'ЗОЛОТО'),
        ('планина', 'ПЛАНИНА'),
        ('серебро', 'СЕРЕБРО'),
        ('новичок', 'НОВИЧОК'),
    )

    status = models.CharField(max_length=32, choices=STATUS_USER, default='новичок')

    def __str__(self):  # Corrected to __str__
        return f"{self.first_name} {self.last_name}"


class Categories(models.Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=32)
    category = models.ForeignKey(Categories, related_name='products', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField()
    date = models.DateField(auto_now=True)
    active = models.BooleanField(verbose_name='в наличии', default=True)
    product_video = models.FileField(upload_to='vid/', verbose_name='Видео', null=True, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} - {self.created_date}"

    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.items.all())
        discount = 0

        if self.user.status == 'золото':
            discount = 0.75
        elif self.user.status == 'планина':
            discount = 0.5
        elif self.user.status == 'серебро':
            discount = 0.25
        elif self.user.status == 'новичок':
            discount = 0

        final_price = total_price * (1 - discount)
        return final_price



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.cart} - {self.product}"

    def get_total_price(self):
        return self.product.price * self.quantity


class ProductPhotos(models.Model):
    product = models.ForeignKey(Product, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Photo for {self.product}"


class Rating(models.Model):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Рейтинг')

    def __str__(self):
        return f"{self.product} - {self.user} - {self.stars} stars"


class Review(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    parent_review = models.ForeignKey('self', related_name='replies', null=True, blank=True,
                                      on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.product}'
