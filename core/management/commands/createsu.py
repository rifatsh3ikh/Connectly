from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Create superuser automatically"

    def handle(self, *args, **kwargs):
        username = os.environ.get("DJANGO_SU_NAME")
        email = os.environ.get("DJANGO_SU_EMAIL")
        password = os.environ.get("DJANGO_SU_PASSWORD")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS("Superuser created"))
        else:
            self.stdout.write("Superuser already exists")
