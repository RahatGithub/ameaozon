from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Create demo admin and regular user for portfolio showcase'

    def handle(self, *args, **options):
        # Admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@ameaozon.com',
                'is_staff': True,
                'is_superuser': True,
                'user_type': User.ADMIN,
            },
        )
        if created:
            admin.set_password('Admin@2026')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin user: admin / Admin@2026'))
        else:
            self.stdout.write(self.style.WARNING('Admin user "admin" already exists'))

        # Regular user
        user, created = User.objects.get_or_create(
            username='rahat',
            defaults={
                'email': 'rahat@ameaozon.com',
                'user_type': User.CUSTOMER,
            },
        )
        if created:
            user.set_password('Rahat@2026')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created regular user: rahat / Rahat@2026'))
        else:
            self.stdout.write(self.style.WARNING('Regular user "rahat" already exists'))
