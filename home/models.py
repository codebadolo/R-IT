from django.db import models
from django.utils.text import slugify
# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
#Front Big Slider
class SliderArea(models.Model):
    image = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None)
    title = models.CharField(max_length=200)
    discount = models.PositiveIntegerField()
    product_url = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.title

class DisplayHotProductInCategories(models.Model):
    image = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None)
    title = models.CharField(max_length=200)
    categories = models.ForeignKey("products.Categories",  on_delete=models.DO_NOTHING)
    product_url = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class PopularCategories(models.Model):
    image = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None)
    categories = models.ForeignKey("products.Categories",  on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categories.name
    
# home/models.py
class NewArrival(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    arrival_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title    

    
# home/models.py
class CustomerReview(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.product.title}"    


# home/models.py
class FlashSale(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.product.title} - {self.discount_percentage}%"
# home/models.py
class FeaturedCategory(models.Model):
    category = models.ForeignKey('products.Categories', on_delete=models.CASCADE)
    featured_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category.name
# home/models.py
class BlogHighlight(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# home/models.py
class NewsletterSignup(models.Model):
    email = models.EmailField(unique=True)
    signup_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email    