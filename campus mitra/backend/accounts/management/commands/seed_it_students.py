from django.core.management.base import BaseCommand
from accounts.models import User, StudentProfile


IT_STUDENTS = [
    ('Yash',      'Tolani',    '2022IT001'),
    ('Shivanand', 'Choure',    '2022IT002'),
    ('Amish',     'Paliwal',   '2022IT003'),
    ('Prince',    'Chohan',    '2022IT004'),
    ('Mayank',    'Malawanta', '2022IT005'),
    ('Aditya',    'Thatte',    '2022IT006'),
    ('Sheetal',   'Khedia',    '2022IT007'),
    ('Palak',     'Shukla',    '2022IT008'),
    ('Shreya',    'Tiwari',    '2022IT009'),
    ('Khushboo',  'Walwani',   '2022IT010'),
]


class Command(BaseCommand):
    help = 'Seed IT branch 6th sem students'

    def handle(self, *args, **kwargs):
        for first, last, enroll in IT_STUDENTS:
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
                branch='IT',
                semester=6,
                section='',
                cgpa=0.0
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created: {first} {last} | {username} | pwd: {password} | {enroll}'
            ))

        self.stdout.write(self.style.SUCCESS('\nAll IT students created!'))
