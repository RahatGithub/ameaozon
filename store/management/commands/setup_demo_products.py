from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, SubCategory, Product
from django.core.files.base import ContentFile
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Setup demo products'

    def handle(self, *args, **kwargs):
        cat_subcats = {
            'Cats': ['Cat Food', 'Cat Toys', 'Cat Accessories', 'Cat Treats'],
            'Dogs': ['Dog Food', 'Dog Toys', 'Dog Accessories', 'Dog Treats'],
            'Birds': ['Bird Food', 'Bird Toys', 'Bird Accessories', 'Bird Treats'],
        }
        
        # Placeholder image links
        image_urls = [
            "https://via.placeholder.com/500x500?text=Pet+Product",
            "https://via.placeholder.com/500x500?text=Cat+Product",
            "https://via.placeholder.com/500x500?text=Dog+Product",
            "https://via.placeholder.com/500x500?text=Bird+Product",
        ]
        
        demo_products = [
            # Cats Products
            {"name": "Premium Cat Food", "description": "High quality nutrition with balanced vitamins and minerals for adult cats. Made with real chicken and fish.", "price": 999.99, "stock": 15},
            {"name": "Kitten Formula", "description": "Special blend for growing kittens with DHA for brain development and extra calcium for strong bones.", "price": 799.99, "stock": 20},
            {"name": "Interactive Cat Toy Mouse", "description": "Battery-operated mouse toy that moves randomly to stimulate your cat's hunting instinct.", "price": 349.99, "stock": 25},
            {"name": "Cat Teaser Wand", "description": "Extendable wand with feathers and bells to provide hours of interactive play with your feline friend.", "price": 249.99, "stock": 30},
            {"name": "Plush Cat Bed", "description": "Ultra-soft round bed with raised edges providing security and comfort for your cat.", "price": 899.99, "stock": 10},
            {"name": "Cat Grooming Brush", "description": "Gentle silicone brush that removes loose fur and stimulates healthy skin and coat.", "price": 299.99, "stock": 35},
            {"name": "Salmon Cat Treats", "description": "Crunchy treats made with real salmon. Perfect for training or rewarding your cat.", "price": 199.99, "stock": 40},
            {"name": "Catnip Treats", "description": "Irresistible treats infused with premium catnip to delight your feline companion.", "price": 249.99, "stock": 30},
            
            # Dogs Products
            {"name": "Organic Dog Food", "description": "All-natural dog food made with organic ingredients, free from artificial colors and preservatives.", "price": 1299.99, "stock": 18},
            {"name": "Puppy Kibble", "description": "Specially formulated small kibble size for puppies with added nutrients for growth and development.", "price": 899.99, "stock": 25},
            {"name": "Squeaky Dog Bone", "description": "Durable rubber bone toy with built-in squeaker for engaging playtime with your dog.", "price": 199.99, "stock": 40},
            {"name": "Rope Tug Toy", "description": "Strong cotton rope toy for interactive play and teeth cleaning. Great for tug-of-war games.", "price": 249.99, "stock": 35},
            {"name": "Orthopedic Dog Bed", "description": "Memory foam bed that provides joint support for dogs of all ages, especially seniors.", "price": 1499.99, "stock": 12},
            {"name": "Reflective Dog Collar", "description": "Adjustable nylon collar with reflective stitching for visibility during night walks.", "price": 399.99, "stock": 28},
            {"name": "Dental Chew Treats", "description": "Textured treats designed to clean teeth and freshen breath while providing a delicious reward.", "price": 349.99, "stock": 30},
            {"name": "Training Treat Pouch", "description": "Small, meaty treats perfect for training sessions, made with real chicken.", "price": 299.99, "stock": 35},
            
            # Birds Products
            {"name": "Premium Bird Seed Mix", "description": "Balanced blend of seeds, grains, and dried fruits suitable for most small to medium-sized birds.", "price": 499.99, "stock": 30},
            {"name": "Parrot Pellet Food", "description": "Nutritionally complete diet formulated specifically for parrots and large birds.", "price": 699.99, "stock": 20},
            {"name": "Bird Swing", "description": "Colorful wooden swing that attaches easily to most cage sizes. Provides exercise and entertainment.", "price": 149.99, "stock": 25},
            {"name": "Mirror Bell Toy", "description": "Bright mirror toy with bell that stimulates bird curiosity and provides mental stimulation.", "price": 99.99, "stock": 40},
            {"name": "Wooden Bird Ladder", "description": "Natural wood ladder that encourages climbing and physical activity for cage birds.", "price": 199.99, "stock": 22},
            {"name": "Bird Cage Cover", "description": "Breathable fabric cover that helps birds maintain a regular sleep cycle by blocking light.", "price": 349.99, "stock": 15},
            {"name": "Honey Treat Sticks", "description": "Sweet honey-based treats that can be hung inside the cage for birds to peck at.", "price": 129.99, "stock": 45},
            {"name": "Mineral Treat Blocks", "description": "Calcium-rich blocks that promote beak health and provide essential minerals.", "price": 89.99, "stock": 50}
        ]
        
        products_created = 0
        
        for cat_name, subcats in cat_subcats.items():
            category = Category.objects.filter(name=cat_name).first()
            if not category:
                self.stdout.write(self.style.WARNING(f'Category {cat_name} not found. Run setup_initial_data first.'))
                continue
                
            for subcat_name in subcats:
                subcat = SubCategory.objects.filter(name=subcat_name, category=category).first()
                if not subcat:
                    self.stdout.write(self.style.WARNING(f'Subcategory {subcat_name} not found.'))
                    continue
                
                for i in range(2):
                    product_index = (i + subcats.index(subcat_name)) % len(demo_products)
                    product_data = demo_products[product_index]
                    
                    product_name = f"{product_data['name']} - {subcat_name}"
                    
                    if not Product.objects.filter(name=product_name, subcategory=subcat).exists():
                        product = Product(
                            subcategory=subcat,
                            name=product_name,
                            slug=slugify(product_name),
                            description=product_data['description'],
                            price=product_data['price'],
                            stock=product_data['stock'],
                            is_available=True
                        )
                        
                        try:
                            img_url = image_urls[(i + subcats.index(subcat_name)) % len(image_urls)]
                            response = requests.get(img_url)
                            if response.status_code == 200:
                                img_temp = BytesIO(response.content)
                                product.image.save(f"{slugify(product_name)}.jpg", ContentFile(img_temp.getvalue()), save=False)
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f'Failed to download image: {e}'))
                        
                        product.save()
                        products_created += 1
                        self.stdout.write(self.style.SUCCESS(f'Created product: {product_name}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {products_created} demo products!'))