import json
from django.core.management.base import BaseCommand
from products.models import (
    Industry, Categories, SubCategories, ProductBrand,
    ProductType, Attribute, AttributeValue, Product,
    ProductInventory, ProductAditionalInformation, ProductImage
)
from Vendors.models import VendorStore
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Upload data to the database'

    def handle(self, *args, **kwargs):
        with open('data.json') as f:
            data = json.load(f)

        for industry_data in data['industries']:
            industry, created = Industry.objects.get_or_create(name=industry_data['name'])
            industry.slug = industry_data.get('slug', slugify(industry.name))
            industry.save()

        for category_data in data['categories']:
            industry = Industry.objects.get(name=category_data.pop('industry'))
            category, created = Categories.objects.get_or_create(name=category_data['name'], industry=industry)
            category.slug = category_data.get('slug', slugify(category.name))
            category.save()

        for subcategory_data in data['subcategories']:
            category = Categories.objects.get(name=subcategory_data.pop('category'))
            base_slug = slugify(subcategory_data['name'])
            slug = base_slug
            counter = 1
            while SubCategories.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            subcategory, created = SubCategories.objects.get_or_create(name=subcategory_data['name'], categories=category, defaults={'slug': slug})

        for product_type_data in data['product_types']:
            ProductType.objects.get_or_create(name=product_type_data['name'], description=product_type_data.get('description'))

        for brand_data in data['brands']:
            brand, created = ProductBrand.objects.get_or_create(name=brand_data['name'])
            brand.description = brand_data.get('description')
            brand.logo = brand_data.get('logo')
            if not brand.slug:
                brand.slug = slugify(brand.name)
            brand.save()

        for attribute_data in data['attributes']:
            product_type = ProductType.objects.get(name=attribute_data.pop('product_type'))
            Attribute.objects.get_or_create(name=attribute_data['name'], product_type=product_type)

        # Create products first
        product_instances = {}
        for product_data in data['products']:
            category = Categories.objects.get(name=product_data.pop('category'))
            subcategory = SubCategories.objects.get(name=product_data.pop('subcategory'), categories=category)
            brand = ProductBrand.objects.get(name=product_data.pop('brand'))
            product_type = ProductType.objects.get(name=product_data.pop('product_type'))
            vendor_store = VendorStore.objects.get(pk=product_data.pop('vendor_store'))
            attributes_data = product_data.pop('attributes')
            images_data = product_data.pop('images')
            additional_info_data = product_data.pop('aditional_information')
            inventory_data = product_data.pop('inventory')

            product_instance, created = Product.objects.get_or_create(
                title=product_data['title'],
                defaults={
                    'regular_price': product_data['regular_price'],
                    'stoc': product_data['stock'],
                    'out_of_stoc': product_data['out_of_stock'],
                    'discounted_parcent': product_data['discounted_percent'],
                    'description': product_data['description'],
                    'modle': product_data['model'],
                    'categories': category,
                    'subcategories': subcategory,
                    'tag': product_data['tag'],
                    'vendor_stores': vendor_store,
                    'details_description': product_data['details_description'],
                    'brand': brand,
                    'product_type': product_type,
                }
            )

            product_instances[product_data['title']] = product_instance

            inventory_instance, created = ProductInventory.objects.get_or_create(
                product=product_instance,
                defaults={
                    'total_quantity': inventory_data['total_quantity'],
                    'available_quantity': inventory_data['available_quantity']
                }
            )

            for image_url in images_data:
                ProductImage.objects.get_or_create(product=product_instance, image=image_url)

            for info_data in additional_info_data:
                ProductAditionalInformation.objects.get_or_create(product=product_instance, **info_data)

        # Create attribute values after products are created
        for attribute_value_data in data['attribute_values']:
            attribute = Attribute.objects.get(name=attribute_value_data.pop('attribute'))
            product = product_instances[attribute_value_data.pop('product')]
            AttributeValue.objects.get_or_create(attribute=attribute, value=attribute_value_data['value'], product=product)

        self.stdout.write(self.style.SUCCESS('Data uploaded successfully'))