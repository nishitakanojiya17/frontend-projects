from django.core.management.base import BaseCommand
from accounts.models import User, StudentProfile


MECHANICAL_STUDENTS = [
    ('Arpit',      'Jaiswal',   '2022ME001'),
    ('Shivam',     'Chouhan',   '2022ME002'),
    ('Sujal',      'Prajapati', '2022ME003'),
    ('Ujjwal',     'Verma',     '2022ME004'),
    ('Ujjwal',     'Tiwari',    '2022ME005'),
    ('Suryansh',   'Verma',     '2022ME006'),
    ('Yash',       'Yadav',     '2022ME007'),
    ('Dheeraj',    'Pal',       '2022ME008'),
    ('Vishal',     'Rathore',   '2022ME009'),
    ('Dhirendra',  'Sisodiya',  '2022ME010'),
    ('Nakshatra',  'Prajapat',  '2022ME011'),
]


class Command(BaseCommand):
    help = 'Seed Mechanical branch 6th sem students'

    def handle(self, *args, **kwargs):
        for first, last, enroll in MECHANICAL_STUDENTS:
            username = f"{first.lower()}.{last.lower()}@iist.ac.in"
            password = f"{first.lower()}@123"

            # Handle duplicate first names (ujjwal x2)
            if User.objects.filter(username=username).exists():
                username = f"{first.lower()}.{last.lower()}.me@iist.ac.in"

            if User.objects.filter(username=username).exists():
                self.stdout.write(f'Already exists: {username}')
                continue

            user = User.objects.create_user(
                username=username,
                email=username,
                password=password,
                first_name=first,
                last_name=last,
                role='student'
            )
            StudentProfile.objects.create(
                user=user,
                enroll_no=enroll,
                branch='ME',
                semester=6,
                section='',
                cgpa=0.0
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created: {first} {last} | {username} | pwd: {password} | {enroll}'
            ))

        self.stdout.write(self.style.SUCCESS('\nAll Mechanical students created!'))
