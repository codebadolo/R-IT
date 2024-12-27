from django.core.management.base import BaseCommand, CommandError
from products.models import ProductBrand

class Command(BaseCommand):
    help = 'Register product brands into the database'

    def handle(self, *args, **kwargs):
        # Hardcoded product brand information
        brands_info = [
            {
                'name': 'Brand 1',
                'description': 'Description for Brand 1',
                'logo': None  # Provide a path to the logo if available
            },
            {
                'name': 'Brand 2',
                'description': 'Description for Brand 2',
                'logo': None  # Provide a path to the logo if available
            },
            # Add more brands as needed
        ]

        for info in brands_info:
            try:
                brand = ProductBrand(
                    name=info['name'],
                    description=info['description'],
                    logo=info['logo']
                )
                brand.save()
                self.stdout.write(self.style.SUCCESS(f'Brand "{info["name"]}" registered successfully'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error registering brand "{info["name"]}": {e}'))