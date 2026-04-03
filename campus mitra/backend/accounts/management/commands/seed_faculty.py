from django.core.management.base import BaseCommand
from accounts.models import User, FacultyProfile


FACULTY = [
    # (first, last, faculty_id, subjects)
    ('Ratnesh',   'Chaturvedi',    'FAC-AIML-001', 'Image & Video Processing'),
    ('Nishant',   'Vijayavargiya', 'FAC-AIML-002', 'Cloud Computing'),
    ('Jaya',      'Singh',         'FAC-AIML-003', 'PDP'),
    ('Smita',     'Marwadi',       'FAC-AIML-004', 'Computer Networks'),
    ('Sukruti',   'Agarwal',       'FAC-AIML-005', 'Minor Project'),
    ('Aatish',    'Mishra',        'FAC-AIML-006', 'Theory of Computation'),
    ('Abhishek',  'Bhatnagar',     'FAC-AIML-007', 'Aptitude'),
    ('Shivani',   'Sharma',        'FAC-AIML-008', 'Competitive Programming'),
]


class Command(BaseCommand):
    help = 'Seed AIML faculty members'

    def handle(self, *args, **kwargs):
        for first, last, fac_id, subjects in FACULTY:
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
                role='faculty'
            )
            FacultyProfile.objects.create(
                user=user,
                faculty_id=fac_id,
                department='AIML',
                subjects=subjects
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created: {first} {last} | {username} | pwd: {password} | {subjects}'
            ))

        self.stdout.write(self.style.SUCCESS('\nAll faculty created!'))
