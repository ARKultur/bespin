import os
from django.core.management.base import BaseCommand

from api.models import Admin, Auth, TwoFactorAuth


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Admin.objects.count() == 0:
            two_fa = TwoFactorAuth(method=1)
            two_fa.save()

            auth = Auth(
                    role=2,
                    email='sheev.palpatine@naboo.net',
                    is_superuser=True,
                    username='the_emperor',
                    first_name='sheev',
                    last_name='palpatine',
                    is_active=True,
                    password='sidious1337',
                    two_factor=two_fa
                )
            auth.save()

            admin = Admin(auth=auth)
            admin.save()

            print(f'[+] Admin user {admin} has been created.')

        else:
            print('[!] Admin user has already been created.')
