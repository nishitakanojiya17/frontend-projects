from django.core.management.base import BaseCommand
from accounts.models import User, FacultyProfile


FACULTY = [
    # (first, last, faculty_id, department, subjects)
    # AIML Faculty
    ('Ratnesh',   'Chaturvedi',    'FAC-AIML-001', 'AIML', 'Image & Video Processing'),
    ('Nishant',   'Vijayavargiya', 'FAC-AIML-002', 'AIML', 'Cloud Computing'),
    ('Jaya',      'Singh',         'FAC-AIML-003', 'AIML', 'PDP'),
    ('Smita',     'Marwadi',       'FAC-AIML-004', 'AIML', 'Computer Networks'),
    ('Sukruti',   'Agarwal',       'FAC-AIML-005', 'AIML', 'Minor Project'),
    ('Aatish',    'Mishra',        'FAC-AIML-006', 'AIML', 'Theory of Computation'),
    ('Abhishek',  'Bhatnagar',     'FAC-AIML-007', 'AIML', 'Aptitude'),
    ('Shivani',   'Sharma',        'FAC-AIML-008', 'AIML', 'Competitive Programming'),
    # Mechanical Faculty
    ('Saurabh',   'Verma',         'FAC-ME-001',   'ME',   'Machine Component Design'),
    ('Rahul',     'Malviya',       'FAC-ME-002',   'ME',   'CAD Lab'),
    ('Umesh',     'Badode',        'FAC-ME-003',   'ME',   'Renewable Energy Technology'),
    ('Devendra',  'Kushwaha',      'FAC-ME-004',   'ME',   'RDBMS Lab'),
    ('Dushyant',  'Sahu',          'FAC-ME-005',   'ME',   'Thermal Engineering'),
    # CS Faculty
    ('Reetu',    'Gupta',     'FAC-CS-001',   'CS',   'Machine Learning'),
    ('Rati',     'Gupta',     'FAC-CS-002',   'CS',   'Computer Networks'),
    ('Shreyas',  'Pagare',    'FAC-CS-003',   'CS',   'Compiler Design'),
    ('Muskan',   'Tirole',    'FAC-CS-004',   'CS',   'DAL'),
    ('Purva',    'Shukla',    'FAC-CS-005',   'CS',   'SDL & Minor Project'),
    ('Gourav',   'Sharma',    'FAC-CS-006',   'CS',   'PDP'),
    ('Ganesh',   'Patidar',   'FAC-CS-007',   'CS',   'Competitive Programming'),
    # IT Faculty
    ('Sheetal',   'Mandloi',   'FAC-IT-001',   'IT',   'Computer Graphics & Multimedia'),
    ('Ankit',     'Saxena',    'FAC-IT-002',   'IT',   'Wireless & Mobile Computing'),
    ('Rakesh',    'Jain',      'FAC-IT-003',   'IT',   'Compiler Design'),
    ('Puneet',    'Duggal',    'FAC-IT-004',   'IT',   'Software Engineering'),
    ('Shreya',    'Dubey',     'FAC-IT-005',   'IT',   'PP'),
    ('Rupal',     'Yadav',     'FAC-IT-006',   'IT',   'Minor Project'),
    ('Mohit',     'Sharma',    'FAC-IT-007',   'IT',   'PDP'),
    ('Varsha',    'Zokarkar',  'FAC-IT-008',   'IT',   'Competitive Programming'),
]


class Command(BaseCommand):
    help = 'Seed all faculty members (AIML + ME)'

    def handle(self, *args, **kwargs):
        for first, last, fac_id, dept, subjects in FACULTY:
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
                department=dept,
                subjects=subjects
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created: {first} {last} | {username} | pwd: {password} | {dept} | {subjects}'
            ))

        self.stdout.write(self.style.SUCCESS('\nAll faculty created!'))
