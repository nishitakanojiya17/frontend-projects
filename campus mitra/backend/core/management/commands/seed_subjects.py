"""
Management command: python manage.py seed_subjects

Seeds all subjects for AIML, CS, IT, ME departments (Sem 6).
Safe to run multiple times — uses get_or_create.
"""
from django.core.management.base import BaseCommand
from core.models import Department, Subject, Faculty

SUBJECTS = {
    'AIML': [
        {'name': 'Image & Video Processing',  'code': 'AIML601'},
        {'name': 'Computer Networks',          'code': 'AIML602'},
        {'name': 'Cloud Computing',            'code': 'AIML603'},
        {'name': 'PDP',                        'code': 'AIML604'},
        {'name': 'Theory of Computation',      'code': 'AIML605'},
        {'name': 'Minor Project',              'code': 'AIML606'},
        {'name': 'Competitive Programming',    'code': 'AIML607'},
        {'name': 'Aptitude',                   'code': 'AIML608'},
    ],
    'CS': [
        {'name': 'Machine Learning',           'code': 'CS601'},
        {'name': 'Computer Networks',          'code': 'CS602'},
        {'name': 'Compiler Design',            'code': 'CS603'},
        {'name': 'DAL',                        'code': 'CS604'},
        {'name': 'SDL & Minor Project',        'code': 'CS605'},
        {'name': 'PDP',                        'code': 'CS606'},
        {'name': 'Competitive Programming',    'code': 'CS607'},
    ],
    'IT': [
        {'name': 'Computer Graphics & Multimedia', 'code': 'IT601'},
        {'name': 'Wireless & Mobile Computing',    'code': 'IT602'},
        {'name': 'Compiler Design',                'code': 'IT603'},
        {'name': 'Software Engineering',           'code': 'IT604'},
        {'name': 'PP',                             'code': 'IT605'},
        {'name': 'Minor Project',                  'code': 'IT606'},
        {'name': 'PDP',                            'code': 'IT607'},
        {'name': 'Competitive Programming',        'code': 'IT608'},
    ],
    'ME': [
        {'name': 'Thermal Engg. & Gas Dynamics',  'code': 'ME601'},
        {'name': 'Machine Component Design',       'code': 'ME602'},
        {'name': 'Turbomachinery',                 'code': 'ME603A'},
        {'name': 'Renewable Energy Technology',    'code': 'ME604C'},
        {'name': 'CAD Lab',                        'code': 'ME605'},
        {'name': 'RDBMS Lab',                      'code': 'ME606'},
        {'name': 'Minor Project II',               'code': 'ME608'},
        {'name': 'PDP',                            'code': 'ME-PDP'},
        {'name': 'Aptitude',                       'code': 'ME-APT'},
    ],
}

# Faculty assignment: faculty_id -> list of subject codes they teach
FACULTY_SUBJECTS = {
    'FAC-AIML-000': ['AIML601'],
    'FAC-AIML-004': ['AIML602'],
    'FAC-AIML-002': ['AIML603'],
    'FAC-AIML-003': ['AIML604'],
    'FAC-AIML-006': ['AIML605'],
    'FAC-AIML-005': ['AIML606'],
    'FAC-AIML-007': ['AIML608'],
    'FAC-AIML-008': ['AIML607'],
    'FAC-CS-001':   ['CS601'],
    'FAC-CS-002':   ['CS602'],
    'FAC-CS-003':   ['CS603'],
    'FAC-CS-004':   ['CS604'],
    'FAC-CS-005':   ['CS605'],
    'FAC-CS-006':   ['CS606'],
    'FAC-CS-007':   ['CS607'],
    'FAC-IT-001':   ['IT601'],
    'FAC-IT-002':   ['IT602'],
    'FAC-IT-003':   ['IT603'],
    'FAC-IT-004':   ['IT604'],
    'FAC-IT-005':   ['IT605'],
    'FAC-IT-006':   ['IT606'],
    'FAC-IT-007':   ['IT607'],
    'FAC-IT-008':   ['IT608'],
    'FAC-ME-001':   ['ME601'],   # Dushyant Sahu — TEGD
    'FAC-ME-002':   ['ME602'],   # Saurabh Verma — MCD
    'FAC-ME-003':   ['ME603A'],  # Umesh Badode — Turbomachinery (Suveer Dubey not in DB yet)
    'FAC-ME-004':   ['ME604C'],  # Umesh Badode — RET
    'FAC-ME-005':   ['ME605'],   # Rahul Malviya — CAD Lab
}


class Command(BaseCommand):
    help = 'Seed all subjects for AIML, CS, IT, ME (Sem 6) and assign faculty'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('=== Seeding Subjects ==='))

        for dept_code, subjects in SUBJECTS.items():
            try:
                dept = Department.objects.get(code=dept_code)
            except Department.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Department {dept_code} not found — run seed_users first'))
                continue

            for s in subjects:
                obj, created = Subject.objects.get_or_create(
                    code=s['code'],
                    defaults={
                        'name': s['name'],
                        'department': dept,
                        'semester': 6,
                    }
                )
                status = 'created' if created else 'exists'
                self.stdout.write(f'  [{status}] {dept_code} · {s["code"]} — {s["name"]}')

        # Assign faculty to subjects
        self.stdout.write(self.style.MIGRATE_HEADING('\n--- Assigning Faculty to Subjects ---'))
        for fac_id, codes in FACULTY_SUBJECTS.items():
            try:
                faculty = Faculty.objects.get(faculty_id=fac_id)
                for code in codes:
                    try:
                        sub = Subject.objects.get(code=code)
                        sub.faculty = faculty
                        sub.save()
                        self.stdout.write(f'  {fac_id} → {code}')
                    except Subject.DoesNotExist:
                        pass
            except Faculty.DoesNotExist:
                pass

        self.stdout.write(self.style.SUCCESS('\n✅ Subjects seeded!'))
        self.stdout.write('   Now run: python manage.py runserver')
