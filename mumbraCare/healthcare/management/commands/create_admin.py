"""
Management command: create_admin

Creates a default superuser for local development / first-time setup.
Skips silently if the user already exists.

Usage:
    python manage.py create_admin
    python manage.py create_admin --username admin --email admin@mumbra.care --password Mumbai@123
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a default admin superuser for Mumbra Care'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin')
        parser.add_argument('--email', default='admin@mumbra.care')
        parser.add_argument('--password', default='Mumbai@123')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(
                f'Admin user "{username}" already exists — skipping.'
            ))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Superuser created:\n'
            f'   Username : {username}\n'
            f'   Email    : {email}\n'
            f'   Password : {password}\n\n'
            f'   ⚠️  Change this password immediately after first login!\n'
            f'   Admin panel: http://127.0.0.1:8000/admin/'
        ))
