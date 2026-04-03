from django.core.management.base import BaseCommand
from accounts.models import User, StudentProfile


STUDENTS = [
    # (first, last, enroll_no)
    ('Nishita',    'Kanojiya',    '2022AIML001'),
    ('Chanchal',   'Rathore',     '2022AIML002'),
    ('Anshika',    'Punase',      '2022AIML003'),
    ('Udit',       'Rathore',     '2022AIML004'),
    ('Keshav',     'Chikhalikar', '2022AIML005'),
    ('Hitanshi',   'Upadhya',     '2022AIML006'),
    ('Shyam',      'Jain',        '2022AIML007'),
    ('Sneha',      'Malviya',     '2022AIML008'),
    ('Nayan',      'Adlak',       '2022AIML009'),
    ('Yash',       'Joshi',       '2022AIML010'),
    ('Adeesh',     'Jain',        '2022AIML011'),
    ('Sumit',      'Singh',       '2022AIML012'),
    ('Shivam',     'Mahajan',     '2022AIML013'),
    ('Bhavesh',    'Prajapat',    '2022AIML014'),
    ('Aaradhya',   'Rassay',      '2022AIML015'),
    ('Bhumika',    'Malakar',     '2022AIML016'),
    ('Samradhi',   'Pawar',       '2022AIML017'),
    ('Anuj',       'Pawar',       '2022AIML018'),
    ('Rishi',      'Singh',       '2022AIML019'),
    ('Nandini',    'Singh',       '2022AIML020'),
]


class Command(BaseCommand):
    help = 'Seed 20 AIML students'

    def handle(self, *args, **kwargs):
        for first, last, enroll in STUDENTS:
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
                branch='AIML',
                semester=6,
                section='B',
                cgpa=0.0
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created: {first} {last} | {username} | pwd: {password} | {enroll}'
            ))

        self.stdout.write(self.style.SUCCESS('\nAll 20 students created!'))
