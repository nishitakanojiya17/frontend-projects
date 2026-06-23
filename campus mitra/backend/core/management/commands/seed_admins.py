"""
Management command: python manage.py seed_admins

Creates two admin accounts for Campus Mitra.
Safe to run multiple times — uses get_or_create.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

ADMINS = [
    {
        'email':      'lokesh.aurangabadkar@iist.ac.in',
        'password':   'lokesh@123',
        'first_name': 'Lokesh',
        'last_name':  'Aurangabadkar',
        'is_staff':   True,
        'is_superuser': True,
    },
    {
        'email':      'keshav.patidar@iist.ac.in',
        'password':   'keshav@123',
        'first_name': 'Keshav',
        'last_name':  'Patidar',
        'is_staff':   True,
        'is_superuser': False,
    },
]


class Command(BaseCommand):
    help = 'Seed two admin accounts for Campus Mitra'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('=== Seeding Admins ==='))

        for a in ADMINS:
            user, created = User.objects.get_or_create(
                username=a['email'],
                defaults={
                    'email':        a['email'],
                    'first_name':   a['first_name'],
                    'last_name':    a['last_name'],
                    'role':         'admin',
                    'is_staff':     a['is_staff'],
                    'is_superuser': a['is_superuser'],
                }
            )
            if created:
                user.set_password(a['password'])
                user.save()

            status = 'created' if created else 'exists'
            self.stdout.write(
                f'  [{status}] {a["first_name"]} {a["last_name"]} | {a["email"]} | password: {a["password"]}'
            )

        self.stdout.write(self.style.SUCCESS('\n✅ Admins seeded!'))
        self.stdout.write('   Login at: login.html → select Admin role')
