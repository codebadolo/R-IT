from django.core.management.base import BaseCommand
from products.models import Product, ProductAditionalInformation, ProductImage

class Command(BaseCommand):
    help = "Populate products and product details"

    def handle(self, *args, **kwargs):
        products = [
            {"product_name": "iPhone 14", "price": 999, "stock": 50, "description": "Latest Apple phone", "sku": "IPH14"},
            {"product_name": "MacBook Pro", "price": 1999, "stock": 20, "description": "Apple laptop for professionals", "sku": "MACPRO"},
            {"product_name": "Nike Air Max", "price": 150, "stock": 200, "description": "Running shoes", "sku": "NIKEAM"},
        ]

        for p in products:
            product, created = Product.objects.get_or_create(
                product_name=p["product_name"],
                price=p["price"],
                stock=p["stock"],
                description=p["description"],
                sku=p["sku"]
            )
            self.stdout.write(self.style.SUCCESS(f"Product '{product.product_name}' created: {created}"))

            # Adding additional information
            ProductAditionalInformation.objects.create(
                product=product,
                info="This is a high-quality product"
            )

            # Adding an image
            ProductImage.objects.create(
                product=product,
                image="sample_image.jpg"
            )
