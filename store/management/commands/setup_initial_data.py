from django.core.management.base import BaseCommand
from store.models import Category, SubCategory
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Setup initial categories and subcategories'

    def handle(self, *args, **kwargs):
        categories_data = [
            {'name': 'Cats'},
            {'name': 'Dogs'},
            {'name': 'Birds'},
        ]

        subcategories_data = {
            'Cats': ['Cat Food', 'Cat Toys', 'Cat Accessories', 'Cat Treats'],
            'Dogs': ['Dog Food', 'Dog Toys', 'Dog Accessories', 'Dog Treats'],
            'Birds': ['Bird Food', 'Bird Toys', 'Bird Accessories', 'Bird Treats'],
        }

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'is_active': True
                }
            )
            
            status = 'Created' if created else 'Already exists'
            self.stdout.write(self.style.SUCCESS(f'{status}: Category "{category.name}"'))
            
            
            for subcat_name in subcategories_data[cat_data['name']]:
                subcat, subcreated = SubCategory.objects.get_or_create(
                    name=subcat_name,
                    category=category,
                    defaults={
                        'slug': slugify(subcat_name),
                        'is_active': True
                    }
                )
                
                substatus = 'Created' if subcreated else 'Already exists'
                self.stdout.write(self.style.SUCCESS(f'  {substatus}: SubCategory "{subcat.name}" under "{category.name}"'))
        
        self.stdout.write(self.style.SUCCESS('Initial setup completed successfully!'))