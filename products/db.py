from django.db import models
from django.db.models import Avg
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import PermissionDenied
import time
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Industry(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Industry, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Categories(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    parent = TreeForeignKey(
        "self",
        on_delete = models.PROTECT,
        related_name = "children",
        null = True,
        blank = True 
        
    )
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Categories, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("categories")
    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ["name"]
#
'''class SubCategories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    categories = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SubCategories, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
'''

class Product(models.Model):
    from Vendors.models import VendorStore

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    regular_price = models.PositiveIntegerField()
    stoc = models.PositiveIntegerField(default=10, verbose_name="Available in Stock")
    out_of_stoc = models.BooleanField(default=False)
    discounted_parcent = models.PositiveIntegerField()
    description = RichTextField(max_length=2000)
    modle = models.CharField(max_length=50)
    """
    in the category section we will work with trees relationsips
    """
    categories = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    tag = models.CharField(max_length=50, help_text="Enter your tag coma separated")
    vendor_stores = models.ForeignKey(VendorStore, on_delete=models.CASCADE, null=True, blank=True)
    details_description = RichTextField(max_length=5000, 
        help_text="Details product description display in the bottom of the product Page. It's help buyer to make deceion on your product")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def discounted_price(self):
        price = (
            self.regular_price - (self.regular_price * self.discounted_parcent) / 100
        )
        # format(price, ".2f")
        return price
    
    @property
    def avarage_review(self):
        all_reviews = ProductStarRatingAndReview.objects.filter(product=self.id).aggregate(avarage=Avg('stars'))
        print(all_reviews)
        return all_reviews
    

    @property
    def total_review_of_product(self):
        total_reviews = ProductStarRatingAndReview.objects.filter(product=self.id)
        return total_reviews
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name 

class ProductAttribute(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description =  models.TextField(blank= True)
    
    def __str__(self):
        return self.name
    
class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    product_type_attributes = models.ManyToManyField(
        ProductAttribute, 
        related_name= "product_type_attributes",
        through="ProductTypeAttribute",
    ) 
    def __str__(self):
        return self.name
    
class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="product_attribute",
        on_delete= models.PROTECT,
    )
    attribute_value = models.CharField(
        max_length=255,
    )

class ProductInventory(models.Model):
    sku = models.CharField(
        max_length=250,
        unique= True,
    )
    upc = models.CharField(
        max_length=12,
        unique= True,
    )
    product_type = models.ForeignKey(
        ProductType , 
        related_name= "product_type",
        on_delete=models.PROTECT
    )
    brand = models.ForeignKey(
        Brand,
        related_name="brand",
        on_delete=models.SET_NULL,
        blank= True,
        null = True
    )
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name="product_attribute_values",
        through="ProductAttributeValues",
    )    
    is_active = models.BooleanField(
        default=False,
    )
    is_default = models.BooleanField(
        default=False,
    )
    retail_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99."),
            },
        },
    )
    store_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99."),
            },
        },
    )
    sale_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99."),
            },
        },
    )
    is_on_sale = models.BooleanField(
        default=False,
    )
    is_digital = models.BooleanField(
        default=False,
    )
    weight = models.FloatField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.sku     
    
    
class Stock(models.Model):
    product_inventory= models.OneToOneField(
        ProductInventory,
        related_name="product_inventory",
        on_delete=models.PROTECT
    )    
    last_checked =  models.DateTimeField(
        null = True,
        blank =True 
    )
    units = models.IntegerField(
        default = 0,
    )
    unit_sold= models.IntegerField(
        default= 0,
    )
    
class ProductImage(models.Model):
    image = models.CharField(max_length=300)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


class ProductAditionalInformation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=70)
    details = models.CharField(max_length=150)

    def __str__(self):
        return self.product.title

class ProductStarRatingAndReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    review_message = models.CharField(max_length=1000)
    review_images = models.ImageField(upload_to=f"product-review-images/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        # if self.review_message[10]:
        #     return self.user.email + self.review_message[10]
        return self.user.email
    


    def save(self, *args, **kwargs):
        if self.user.user_role != '1': # if not Customer 
            raise PermissionDenied('Only Customer can Add Review')
        super().save(*args, **kwargs)
    


class CuponCodeGenaration(models.Model):
    name = models.CharField(max_length=50)
    cupon_code = models.CharField(max_length=50)
    discoun_parcent = models.PositiveIntegerField()
    up_to = models.PositiveIntegerField(help_text="Limit of Discount Amaount")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CustomerAddress(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    state = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    zip_code = models.PositiveIntegerField()
    street_address = models.CharField(max_length=250)
    mobile = models.PositiveIntegerField()
    is_billing = models.BooleanField(default=True)
    is_shipping = models.BooleanField(default=True)

    def __str__(self):
        # return f"{self.state}"
        return f"{self.street_address}, {self.zip_code}, {self.city}, {self.state}"


class Cart(models.Model):
    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="customer_with_product_in_cart",
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    shipping_address = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE, null=True, blank=True)
    cupon_applaied = models.BooleanField(default=False)
    cupon_code = models.ForeignKey(
        CuponCodeGenaration,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    last_updated = models.DateTimeField(auto_now_add=True)

    @property
    def total_product_price(self):
        price = self.product.discounted_price * self.quantity
        # price = f"{price:.2f}"
        return price

    @classmethod
    def subtotal_product_price(cls, user):
        carts = Cart.objects.filter(user=user)
        subtotal_price = 0.00
        if carts:
            subtotal_price = sum(cart.total_product_price for cart in carts)
        if carts:
            cart_item = carts[0]
            if cart_item.cupon_applaied:
                subtotal_price = subtotal_price - (
                    cart_item.cupon_code.discoun_parcent * subtotal_price / 100
                )

        return subtotal_price

    def __str__(self):
        return self.product.title




class PlacedOder(models.Model):
    STATUS = [
        ("Oder Recived", "Oder Recived"),
        ("Oder Packed", "Oder Packed"),
        ("Oder OnTheWay", "Oder OnTheWay"),
        ("Oder Shipped", "Oder Shipped"),
    ]
    # order_number = models.BigAutoField()
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(
        CustomerAddress, on_delete=models.DO_NOTHING, related_name="shipping_address"
    )
    sub_total_price = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS, default="Oder Recived")
    paid = models.BooleanField(default=False)
    placed_date = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=12, blank=True, null=True)

    @property
    def oder_id(self):
        return f"OID{str(self.id).zfill(6)}"

    def save(self, *args, **kwargs):
        self.order_number = self.oder_id
        super(PlacedOder, self).save(*args, **kwargs)

    @classmethod
    def placed_oders_by_user(cls, user):
        oders = PlacedOder.objects.filter(user=user)
        placed_oder_items_dict = {}

        for oder in oders:
            placed_oder_list = []

            placed_oder_details = {}
            placed_oder_details["sub_total_price"] = oder.sub_total_price
            placed_oder_details["status"] = oder.status
            placed_oder_details["placed_date"] = oder.placed_date
            placed_oder_details["paid"] = oder.paid
            placed_oder_list.append(placed_oder_details)

            oder_items = PlacedeOderItem.objects.filter(placed_oder=oder)

            for item in oder_items:
                oder_items_list = []
                # print(item.product.title)
                # Checking if product image exists before accessing it
                product_image = item.product.productimage_set.first()
                if product_image:
                    image = product_image.image
                    oder_items_list.append(image)
                else:
                    # Append None or any default image if no image is found
                    oder_items_list.append('https://placehold.co/200x200')
                title = item.product.title
                quantity = item.quantity
                total_price = item.total_price
                oder_items_list.append(title)
                oder_items_list.append(quantity)
                oder_items_list.append(total_price)
                placed_oder_list.append(oder_items_list)

            placed_oder_items_dict[oder.oder_id] = placed_oder_list
        return placed_oder_items_dict
        # return 'fg'

    def __str__(self):
        return self.order_number


class PlacedeOderItem(models.Model):
    placed_oder = models.ForeignKey(
        PlacedOder, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    total_price = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.discounted_price
        super(PlacedeOderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.placed_oder.user.first_name}--{str(self.placed_oder.id)}--{str(self.placed_oder.placed_date)}"


class CompletedOder(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE)
    sub_total_price = models.FloatField()
    status = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    complete_date = models.DateTimeField(auto_now_add=True)
    oder_number = models.CharField(max_length=12)

    def __str__(self):
        return self.oder_number


class CompletedOderItems(models.Model):
    completed_oder = models.ForeignKey(
        CompletedOder, on_delete=models.CASCADE, related_name="delivered_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="delivered_product")
    quantity = models.PositiveIntegerField()
    total_price = models.FloatField()

    def __str__(self):
        return self.product.title[:20] + str(self.product.id)
