from django.core.management.base import BaseCommand
from accounts.models import User, StudentProfile, FacultyProfile, ParentProfile


class Command(BaseCommand):
    help = 'Create demo users for Campus Mitra'

    def handle(self, *args, **kwargs):
        # Student
        if not User.objects.filter(username='student@iist.ac.in').exists():
            u = User.objects.create_user(
                username='student@iist.ac.in',
                email='student@iist.ac.in',
                password='student123',
                first_name='Udit',
                last_name='Rathod',
                role='student'
            )
            StudentProfile.objects.create(
                user=u, enroll_no='2022AIML045',
                branch='AIML', semester=6, section='B', cgpa=8.4
            )
            self.stdout.write(self.style.SUCCESS('Created student: student@iist.ac.in'))

        # Faculty
        if not User.objects.filter(username='faculty@iist.ac.in').exists():
            u = User.objects.create_user(
                username='faculty@iist.ac.in',
                email='faculty@iist.ac.in',
                password='faculty123',
                first_name='Smita',
                last_name='Marwadi',
                role='faculty'
            )
            FacultyProfile.objects.create(
                user=u, faculty_id='FAC-AIML-001',
                department='AIML', subjects='Computer Networks'
            )
            self.stdout.write(self.style.SUCCESS('Created faculty: faculty@iist.ac.in'))

        # Admin
        if not User.objects.filter(username='admin@iist.ac.in').exists():
            u = User.objects.create_user(
                username='admin@iist.ac.in',
                email='admin@iist.ac.in',
                password='admin123',
                first_name='Arvind',
                last_name='Singh',
                role='admin',
                is_staff=True
            )
            self.stdout.write(self.style.SUCCESS('Created admin: admin@iist.ac.in'))

        # Parent
        if not User.objects.filter(username='parent@iist.ac.in').exists():
            student = StudentProfile.objects.filter(enroll_no='2022AIML045').first()
            u = User.objects.create_user(
                username='parent@iist.ac.in',
                email='parent@iist.ac.in',
                password='parent123',
                first_name='Sunita',
                last_name='Verma',
                role='parent'
            )
            ParentProfile.objects.create(user=u, child=student)
            self.stdout.write(self.style.SUCCESS('Created parent: parent@iist.ac.in'))

        self.stdout.write(self.style.SUCCESS('Done! All demo users created.'))
