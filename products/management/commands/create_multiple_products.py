from django.core.management.base import BaseCommand
from products.models import Product, Categories, ProductBrand, ProductType, ProductInventory, Attribute, AttributeValue, VendorStore
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Create multiple products with associated details'

    def add_arguments(self, parser):
        # Adding an optional argument for industry_id
        parser.add_argument('--industry_id', type=int, help='ID of the industry to associate with categories')

    def handle(self, *args, **options):
        industry_id = options['industry_id']  # Retrieve the industry_id argument
        if not industry_id:
            self.stdout.write(self.style.ERROR('industry_id argument is required!'))
            return
        
        # Sample product details (replace with your actual data)
        products_data = [
            {"title": "Product 1", "regular_price": 100, "discounted_price": 80, "description": "Description 1", "category_name": "Category 1", "vendor_store_name": "Vendor 1", "brand_name": "Brand 1", "product_type_name": "Type 1", "attributes": ["Color: Red"]},
            # Add more product data here...
        ]
        
        for product_data in products_data:
            self.create_product(
                title=product_data['title'],
                regular_price=product_data['regular_price'],
                discounted_price=product_data['discounted_price'],
                description=product_data['description'],
                category_name=product_data['category_name'],
                vendor_store_name=product_data['vendor_store_name'],
                brand_name=product_data['brand_name'],
                product_type_name=product_data['product_type_name'],
                attributes=product_data['attributes'],
                industry_id=industry_id  # Pass the industry_id
            )
            
    def create_product(self, title, regular_price, discounted_price, description, category_name, vendor_store_name, brand_name, product_type_name, attributes, industry_id):
        # Fetch or create the necessary models
        category, _ = Categories.objects.get_or_create(
            name=category_name,
            defaults={'industry_id': industry_id}  # Use the passed industry_id
        )
        vendor_store = VendorStore.objects.get(name=vendor_store_name)
        brand, _ = ProductBrand.objects.get_or_create(name=brand_name)
        product_type, _ = ProductType.objects.get_or_create(name=product_type_name)
        
        # Create the product
        product = Product(
            title=title,
            regular_price=regular_price,
            discounted_parcent=((regular_price - discounted_price) / regular_price) * 100,
            description=description,
            categories=category,
            vendor_stores=vendor_store,
            brand=brand,
            product_type=product_type
        )
        product.save()

        # Create product inventory
        inventory = ProductInventory(
            product=product,
            total_quantity=100,
            available_quantity=100
        )
        inventory.save()

        # Add attributes to the product
        for attribute_name in attributes:
            attribute, created = Attribute.objects.get_or_create(name=attribute_name)
            attribute_value, created = AttributeValue.objects.get_or_create(attribute=attribute, value=attribute_name)
            product.attributes.add(attribute)
        
        product.save()
        self.stdout.write(self.style.SUCCESS(f'Product {title} created successfully!'))
