from django.core.management.base import BaseCommand
from accounts.models import User, StudentProfile


CS_STUDENTS = [
    # (first, last, enroll_no)
    ('Riya',       'Sharma',     '2022CS001'),
    ('Rohan',      'Gupta',      '2022CS002'),
    ('Saakshi',    'Pardeshi',   '2022CS003'),
    ('Sachin',     'Tiwari',     '2022CS004'),
    ('Sagar',      'Patel',      '2022CS005'),
    ('Sahil',      'Khan',       '2022CS006'),
    ('Sahvendra',  'Singh',      '2022CS007'),
    ('Samyak',     'Jain',       '2022CS008'),
    ('Sanidhya',   'Verma',      '2022CS009'),
    ('Sanjeet',    'Yadav',      '2022CS010'),
]


class Command(BaseCommand):
    help = 'Seed CS branch 6th sem students'

    def handle(self, *args, **kwargs):
        for first, last, enroll in CS_STUDENTS:
            username = f"{first.lower()}.{last.lower()}@iist.ac.in"
            password = f"{first.lower()}@123"

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
                branch='CS',
                semester=6,
                section='',
                cgpa=0.0
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created: {first} {last} | {username} | pwd: {password} | {enroll}'
            ))

        self.stdout.write(self.style.SUCCESS('\nAll CS students created!'))
