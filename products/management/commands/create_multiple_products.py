from django.core.management.base import BaseCommand, CommandError
from products.models import Product, Categories, SubCategories, ProductBrand, ProductType
from Vendors.models import  VendorStore
class Command(BaseCommand):
    help = 'Register products into the database'

    def handle(self, *args, **kwargs):
        # Ensure related objects exist
        brand, created = ProductBrand.objects.get_or_create(
            id=1,
            defaults={'name': 'Default Brand', 'slug': 'default-brand'}
        )

        category, created = Categories.objects.get_or_create(
            id=1,
            defaults={'name': 'Default Category', 'slug': 'default-category'}
        )

        subcategory, created = SubCategories.objects.get_or_create(
            id=1,
            categories=category,
            defaults={'name': 'Default SubCategory', 'slug': 'default-subcategory'}
        )

        vendor_store, created = VendorStore.objects.get_or_create(
            id=1,
            defaults={'name': 'Default Vendor Store'}
        )

        product_type, created = ProductType.objects.get_or_create(
            id=1,
            defaults={'name': 'Default Product Type'}
        )

        # Hardcoded product information
        products_info = [
            {
                'title': 'Product 1',
                'regular_price': 100,
                'discounted_parcent': 10,
                'description': 'Description for Product 1',
                'modle': 'Model1',
                'categories': category,
                'subcategories': subcategory,
                'tag': 'tag1',
                'vendor_stores': vendor_store,
                'details_description': 'Detailed description for Product 1',
                'brand': brand,
                'product_type': product_type
            },
            # Add more products as needed
        ]

        for info in products_info:
            try:
                product = Product(
                    title=info['title'],
                    regular_price=info['regular_price'],
                    discounted_parcent=info['discounted_parcent'],
                    description=info['description'],
                    modle=info['modle'],
                    categories=info['categories'],
                    subcategories=info['subcategories'],
                    tag=info['tag'],
                    vendor_stores=info['vendor_stores'],
                    details_description=info['details_description'],
                    brand=info['brand'],
                    product_type=info['product_type']
                )
                product.save()
                self.stdout.write(self.style.SUCCESS(f'Product "{info["title"]}" registered successfully'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error registering product "{info["title"]}": {e}'))