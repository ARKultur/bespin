"""Initiates first user on bare deployments"""
from django.core.management.base import BaseCommand

from api.models import Admin, Auth


class Command(BaseCommand):
    """Command creating the first user (admin) if database does not have any."""
    def handle(self, *_, **__):
        if Admin.objects.count() == 0:
            auth = Auth(
                    role=2,
                    email='sheev.palpatine@naboo.net',
                    is_superuser=True,
                    username='the_emperor',
                    first_name='sheev',
                    last_name='palpatine',
                    is_active=True,
                    password='sidious1337',
                )
            auth.save()

            admin = Admin(auth=auth)
            admin.save()

            print(f'[+] Admin user {admin} has been created.')

        else:
            print('[!] Admin user has already been created.')
