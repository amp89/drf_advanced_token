from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Understand that this logs out all users',
        )

    def handle(self, *args, **options):
        
        if not options["force"]:
            print("Include --force if you understand that this will log out all users.")
        else:
            Token.objects.all().delete()
            print("All auth tokens deleted.")

