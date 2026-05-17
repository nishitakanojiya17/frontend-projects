"""
Management command: python manage.py seed_users

Creates all departments, students, and faculty from CREDENTIALS.md.
Safe to run multiple times — uses get_or_create throughout.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Department, Student, Faculty, Parent

User = get_user_model()


# ── Departments ───────────────────────────────────────────────────────────────

DEPARTMENTS = [
    {'name': 'Artificial Intelligence & Machine Learning', 'code': 'AIML'},
    {'name': 'Computer Science & Engineering',             'code': 'CS'},
    {'name': 'Information Technology',                     'code': 'IT'},
    {'name': 'Mechanical Engineering',                     'code': 'ME'},
]


# ── Students ──────────────────────────────────────────────────────────────────

STUDENTS = [
    # AIML
    {'enrollment': '2022AIML001', 'first': 'Nishita',   'last': 'Kanojiya',     'email': 'nishita.kanojiya@iist.ac.in',     'password': 'nishita@123',   'dept': 'AIML'},
    {'enrollment': '2022AIML002', 'first': 'Chanchal',  'last': 'Rathore',      'email': 'chanchal.rathore@iist.ac.in',     'password': 'chanchal@123',  'dept': 'AIML'},
    {'enrollment': '2022AIML003', 'first': 'Anshika',   'last': 'Punase',       'email': 'anshika.punase@iist.ac.in',       'password': 'anshika@123',   'dept': 'AIML'},
    {'enrollment': '2022AIML004', 'first': 'Udit',      'last': 'Rathore',      'email': 'udit.rathore@iist.ac.in',         'password': 'udit@123',      'dept': 'AIML'},
    {'enrollment': '2022AIML005', 'first': 'Keshav',    'last': 'Chikhalikar',  'email': 'keshav.chikhalikar@iist.ac.in',   'password': 'keshav@123',    'dept': 'AIML'},
    {'enrollment': '2022AIML006', 'first': 'Hitanshi',  'last': 'Upadhya',      'email': 'hitanshi.upadhya@iist.ac.in',     'password': 'hitanshi@123',  'dept': 'AIML'},
    {'enrollment': '2022AIML007', 'first': 'Shyam',     'last': 'Jain',         'email': 'shyam.jain@iist.ac.in',           'password': 'shyam@123',     'dept': 'AIML'},
    {'enrollment': '2022AIML008', 'first': 'Sneha',     'last': 'Malviya',      'email': 'sneha.malviya@iist.ac.in',        'password': 'sneha@123',     'dept': 'AIML'},
    {'enrollment': '2022AIML009', 'first': 'Nayan',     'last': 'Adlak',        'email': 'nayan.adlak@iist.ac.in',          'password': 'nayan@123',     'dept': 'AIML'},
    {'enrollment': '2022AIML010', 'first': 'Yash',      'last': 'Joshi',        'email': 'yash.joshi@iist.ac.in',           'password': 'yash@123',      'dept': 'AIML'},
    {'enrollment': '2022AIML011', 'first': 'Adeesh',    'last': 'Jain',         'email': 'adeesh.jain@iist.ac.in',          'password': 'adeesh@123',    'dept': 'AIML'},
    {'enrollment': '2022AIML012', 'first': 'Sumit',     'last': 'Singh',        'email': 'sumit.singh@iist.ac.in',          'password': 'sumit@123',     'dept': 'AIML'},
    {'enrollment': '2022AIML013', 'first': 'Shivam',    'last': 'Mahajan',      'email': 'shivam.mahajan@iist.ac.in',       'password': 'shivam@123',    'dept': 'AIML'},
    {'enrollment': '2022AIML014', 'first': 'Bhavesh',   'last': 'Prajapat',     'email': 'bhavesh.prajapat@iist.ac.in',     'password': 'bhavesh@123',   'dept': 'AIML'},
    {'enrollment': '2022AIML015', 'first': 'Aaradhya',  'last': 'Rassay',       'email': 'aaradhya.rassay@iist.ac.in',      'password': 'aaradhya@123',  'dept': 'AIML'},
    {'enrollment': '2022AIML016', 'first': 'Bhumika',   'last': 'Malakar',      'email': 'bhumika.malakar@iist.ac.in',      'password': 'bhumika@123',   'dept': 'AIML'},
    {'enrollment': '2022AIML017', 'first': 'Samradhi',  'last': 'Pawar',        'email': 'samradhi.pawar@iist.ac.in',       'password': 'samradhi@123',  'dept': 'AIML'},
    {'enrollment': '2022AIML018', 'first': 'Anuj',      'last': 'Pawar',        'email': 'anuj.pawar@iist.ac.in',           'password': 'anuj@123',      'dept': 'AIML'},
    {'enrollment': '2022AIML019', 'first': 'Rishi',     'last': 'Singh',        'email': 'rishi.singh@iist.ac.in',          'password': 'rishi@123',     'dept': 'AIML'},
    {'enrollment': '2022AIML020', 'first': 'Nandini',   'last': 'Singh',        'email': 'nandini.singh@iist.ac.in',        'password': 'nandini@123',   'dept': 'AIML'},
    # CS
    {'enrollment': '2022CS001',   'first': 'Riya',      'last': 'Sharma',       'email': 'riya.sharma@iist.ac.in',          'password': 'riya@123',      'dept': 'CS'},
    {'enrollment': '2022CS002',   'first': 'Rohan',     'last': 'Gupta',        'email': 'rohan.gupta@iist.ac.in',          'password': 'rohan@123',     'dept': 'CS'},
    {'enrollment': '2022CS003',   'first': 'Saakshi',   'last': 'Pardeshi',     'email': 'saakshi.pardeshi@iist.ac.in',     'password': 'saakshi@123',   'dept': 'CS'},
    {'enrollment': '2022CS004',   'first': 'Sachin',    'last': 'Tiwari',       'email': 'sachin.tiwari@iist.ac.in',        'password': 'sachin@123',    'dept': 'CS'},
    {'enrollment': '2022CS005',   'first': 'Sagar',     'last': 'Patel',        'email': 'sagar.patel@iist.ac.in',          'password': 'sagar@123',     'dept': 'CS'},
    {'enrollment': '2022CS006',   'first': 'Sahil',     'last': 'Khan',         'email': 'sahil.khan@iist.ac.in',           'password': 'sahil@123',     'dept': 'CS'},
    {'enrollment': '2022CS007',   'first': 'Sahvendra',  'last': 'Singh',       'email': 'sahvendra.singh@iist.ac.in',      'password': 'sahvendra@123', 'dept': 'CS'},
    {'enrollment': '2022CS008',   'first': 'Samyak',    'last': 'Jain',         'email': 'samyak.jain@iist.ac.in',          'password': 'samyak@123',    'dept': 'CS'},
    {'enrollment': '2022CS009',   'first': 'Sanidhya',  'last': 'Verma',        'email': 'sanidhya.verma@iist.ac.in',       'password': 'sanidhya@123',  'dept': 'CS'},
    {'enrollment': '2022CS010',   'first': 'Sanjeet',   'last': 'Yadav',        'email': 'sanjeet.yadav@iist.ac.in',        'password': 'sanjeet@123',   'dept': 'CS'},
    # IT
    {'enrollment': '2022IT001',   'first': 'Yash',      'last': 'Tolani',       'email': 'yash.tolani@iist.ac.in',          'password': 'yash@123',      'dept': 'IT'},
    {'enrollment': '2022IT002',   'first': 'Shivanand', 'last': 'Choure',       'email': 'shivanand.choure@iist.ac.in',     'password': 'shivanand@123', 'dept': 'IT'},
    {'enrollment': '2022IT003',   'first': 'Amish',     'last': 'Paliwal',      'email': 'amish.paliwal@iist.ac.in',        'password': 'amish@123',     'dept': 'IT'},
    {'enrollment': '2022IT004',   'first': 'Prince',    'last': 'Chohan',       'email': 'prince.chohan@iist.ac.in',        'password': 'prince@123',    'dept': 'IT'},
    {'enrollment': '2022IT005',   'first': 'Mayank',    'last': 'Malawanta',    'email': 'mayank.malawanta@iist.ac.in',     'password': 'mayank@123',    'dept': 'IT'},
    {'enrollment': '2022IT006',   'first': 'Aditya',    'last': 'Thatte',       'email': 'aditya.thatte@iist.ac.in',        'password': 'aditya@123',    'dept': 'IT'},
    {'enrollment': '2022IT007',   'first': 'Sheetal',   'last': 'Khedia',       'email': 'sheetal.khedia@iist.ac.in',       'password': 'sheetal@123',   'dept': 'IT'},
    {'enrollment': '2022IT008',   'first': 'Palak',     'last': 'Shukla',       'email': 'palak.shukla@iist.ac.in',         'password': 'palak@123',     'dept': 'IT'},
    {'enrollment': '2022IT009',   'first': 'Shreya',    'last': 'Tiwari',       'email': 'shreya.tiwari@iist.ac.in',        'password': 'shreya@123',    'dept': 'IT'},
    {'enrollment': '2022IT010',   'first': 'Khushboo',  'last': 'Walwani',      'email': 'khushboo.walwani@iist.ac.in',     'password': 'khushboo@123',  'dept': 'IT'},
    # ME
    {'enrollment': '2022ME001',   'first': 'Arpit',     'last': 'Jaiswal',      'email': 'arpit.jaiswal@iist.ac.in',        'password': 'arpit@123',     'dept': 'ME'},
    {'enrollment': '2022ME002',   'first': 'Shivam',    'last': 'Chouhan',      'email': 'shivam.chouhan@iist.ac.in',       'password': 'shivam@123',    'dept': 'ME'},
    {'enrollment': '2022ME003',   'first': 'Sujal',     'last': 'Prajapati',    'email': 'sujal.prajapati@iist.ac.in',      'password': 'sujal@123',     'dept': 'ME'},
    {'enrollment': '2022ME004',   'first': 'Ujjwal',    'last': 'Verma',        'email': 'ujjwal.verma@iist.ac.in',         'password': 'ujjwal@123',    'dept': 'ME'},
    {'enrollment': '2022ME005',   'first': 'Ujjwal',    'last': 'Tiwari',       'email': 'ujjwal.tiwari@iist.ac.in',        'password': 'ujjwal@123',    'dept': 'ME'},
    {'enrollment': '2022ME006',   'first': 'Suryansh',  'last': 'Verma',        'email': 'suryansh.verma@iist.ac.in',       'password': 'suryansh@123',  'dept': 'ME'},
    {'enrollment': '2022ME007',   'first': 'Yash',      'last': 'Yadav',        'email': 'yash.yadav@iist.ac.in',           'password': 'yash@123',      'dept': 'ME'},
    {'enrollment': '2022ME008',   'first': 'Dheeraj',   'last': 'Pal',          'email': 'dheeraj.pal@iist.ac.in',          'password': 'dheeraj@123',   'dept': 'ME'},
    {'enrollment': '2022ME009',   'first': 'Vishal',    'last': 'Rathore',      'email': 'vishal.rathore@iist.ac.in',       'password': 'vishal@123',    'dept': 'ME'},
    {'enrollment': '2022ME010',   'first': 'Dhirendra', 'last': 'Sisodiya',     'email': 'dhirendra.sisodiya@iist.ac.in',   'password': 'dhirendra@123', 'dept': 'ME'},
    {'enrollment': '2022ME011',   'first': 'Nakshatra', 'last': 'Prajapat',     'email': 'nakshatra.prajapat@iist.ac.in',   'password': 'nakshatra@123', 'dept': 'ME'},
]


# ── Faculty ───────────────────────────────────────────────────────────────────

FACULTY = [
    # AIML
    {'fid': 'FAC-AIML-000', 'first': 'Ratnesh',   'last': 'Chaturvedi',    'email': 'ratnesh.chaturvedi@iist.ac.in',   'password': 'ratnesh@123',   'dept': 'AIML', 'designation': 'Professor'},
    {'fid': 'FAC-AIML-001', 'first': 'Smita',     'last': 'Marwadi',       'email': 'faculty@iist.ac.in',              'password': 'faculty123',    'dept': 'AIML', 'designation': 'Associate Professor'},
    {'fid': 'FAC-AIML-002', 'first': 'Nishant',   'last': 'Vijayavargiya', 'email': 'nishant.vijayavargiya@iist.ac.in','password': 'nishant@123',   'dept': 'AIML', 'designation': 'Assistant Professor'},
    {'fid': 'FAC-AIML-003', 'first': 'Jaya',      'last': 'Singh',         'email': 'jaya.singh@iist.ac.in',           'password': 'jaya@123',      'dept': 'AIML', 'designation': 'Assistant Professor'},
    {'fid': 'FAC-AIML-004', 'first': 'Smita',     'last': 'Marwadi',       'email': 'smita.marwadi@iist.ac.in',        'password': 'smita@123',     'dept': 'AIML', 'designation': 'Associate Professor'},
    {'fid': 'FAC-AIML-005', 'first': 'Sukruti',   'last': 'Agarwal',       'email': 'sukruti.agarwal@iist.ac.in',      'password': 'sukruti@123',   'dept': 'AIML', 'designation': 'Assistant Professor'},
    {'fid': 'FAC-AIML-006', 'first': 'Aatish',    'last': 'Mishra',        'email': 'aatish.mishra@iist.ac.in',        'password': 'aatish@123',    'dept': 'AIML', 'designation': 'Assistant Professor'},
    {'fid': 'FAC-AIML-007', 'first': 'Abhishek',  'last': 'Bhatnagar',     'email': 'abhishek.bhatnagar@iist.ac.in',   'password': 'abhishek@123',  'dept': 'AIML', 'designation': 'Assistant Professor'},
    {'fid': 'FAC-AIML-008', 'first': 'Shivani',   'last': 'Sharma',        'email': 'shivani.sharma@iist.ac.in',       'password': 'shivani@123',   'dept': 'AIML', 'designation': 'Assistant Professor'},
    # CS
    {'fid': 'FAC-CS-001',   'first': 'Reetu',     'last': 'Gupta',         'email': 'reetu.gupta@iist.ac.in',          'password': 'reetu@123',     'dept': 'CS',   'designation': 'Associate Professor'},
    {'fid': 'FAC-CS-002',   'first': 'Rati',      'last': 'Gupta',         'email': 'rati.gupta@iist.ac.in',           'password': 'rati@123',      'dept': 'CS',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-CS-003',   'first': 'Shreyas',   'last': 'Pagare',        'email': 'shreyas.pagare@iist.ac.in',       'password': 'shreyas@123',   'dept': 'CS',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-CS-004',   'first': 'Muskan',    'last': 'Tirole',        'email': 'muskan.tirole@iist.ac.in',        'password': 'muskan@123',    'dept': 'CS',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-CS-005',   'first': 'Purva',     'last': 'Shukla',        'email': 'purva.shukla@iist.ac.in',         'password': 'purva@123',     'dept': 'CS',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-CS-006',   'first': 'Gourav',    'last': 'Sharma',        'email': 'gourav.sharma@iist.ac.in',        'password': 'gourav@123',    'dept': 'CS',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-CS-007',   'first': 'Ganesh',    'last': 'Patidar',       'email': 'ganesh.patidar@iist.ac.in',       'password': 'ganesh@123',    'dept': 'CS',   'designation': 'Assistant Professor'},
    # IT
    {'fid': 'FAC-IT-001',   'first': 'Sheetal',   'last': 'Mandloi',       'email': 'sheetal.mandloi@iist.ac.in',      'password': 'sheetal@123',   'dept': 'IT',   'designation': 'Associate Professor'},
    {'fid': 'FAC-IT-002',   'first': 'Ankit',     'last': 'Saxena',        'email': 'ankit.saxena@iist.ac.in',         'password': 'ankit@123',     'dept': 'IT',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-IT-003',   'first': 'Rakesh',    'last': 'Jain',          'email': 'rakesh.jain@iist.ac.in',          'password': 'rakesh@123',    'dept': 'IT',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-IT-004',   'first': 'Puneet',    'last': 'Duggal',        'email': 'puneet.duggal@iist.ac.in',        'password': 'puneet@123',    'dept': 'IT',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-IT-005',   'first': 'Shreya',    'last': 'Dubey',         'email': 'shreya.dubey@iist.ac.in',         'password': 'shreya@123',    'dept': 'IT',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-IT-006',   'first': 'Rupal',     'last': 'Yadav',         'email': 'rupal.yadav@iist.ac.in',          'password': 'rupal@123',     'dept': 'IT',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-IT-007',   'first': 'Mohit',     'last': 'Sharma',        'email': 'mohit.sharma@iist.ac.in',         'password': 'mohit@123',     'dept': 'IT',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-IT-008',   'first': 'Varsha',    'last': 'Zokarkar',      'email': 'varsha.zokarkar@iist.ac.in',      'password': 'varsha@123',    'dept': 'IT',   'designation': 'Assistant Professor'},
    # ME
    {'fid': 'FAC-ME-001',   'first': 'Saurabh',   'last': 'Verma',         'email': 'saurabh.verma@iist.ac.in',        'password': 'saurabh@123',   'dept': 'ME',   'designation': 'Associate Professor'},
    {'fid': 'FAC-ME-002',   'first': 'Rahul',     'last': 'Malviya',       'email': 'rahul.malviya@iist.ac.in',        'password': 'rahul@123',     'dept': 'ME',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-ME-003',   'first': 'Umesh',     'last': 'Badode',        'email': 'umesh.badode@iist.ac.in',         'password': 'umesh@123',     'dept': 'ME',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-ME-004',   'first': 'Devendra',  'last': 'Kushwaha',      'email': 'devendra.kushwaha@iist.ac.in',    'password': 'devendra@123',  'dept': 'ME',   'designation': 'Assistant Professor'},
    {'fid': 'FAC-ME-005',   'first': 'Dushyant',  'last': 'Sahu',          'email': 'dushyant.sahu@iist.ac.in',        'password': 'dushyant@123',  'dept': 'ME',   'designation': 'Assistant Professor'},
]


# ── Demo / Admin accounts ─────────────────────────────────────────────────────

DEMO_ACCOUNTS = [
    {'email': 'student@iist.ac.in', 'password': 'student123', 'role': 'student',
     'first': 'Demo', 'last': 'Student'},
    {'email': 'parent@iist.ac.in',  'password': 'parent123',  'role': 'parent',
     'first': 'Demo', 'last': 'Parent'},
    {'email': 'admin@iist.ac.in',   'password': 'admin123',   'role': 'admin',
     'first': 'Admin', 'last': 'IIST', 'is_staff': True, 'is_superuser': True},
]


class Command(BaseCommand):
    help = 'Seed all departments, students, faculty, and demo accounts from CREDENTIALS.md'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('=== Campus Mitra Seed ==='))

        # 1. Departments
        dept_map = {}
        for d in DEPARTMENTS:
            obj, created = Department.objects.get_or_create(code=d['code'], defaults={'name': d['name']})
            dept_map[d['code']] = obj
            status = 'created' if created else 'exists'
            self.stdout.write(f"  Dept [{status}]: {obj.name}")

        # 2. Students
        self.stdout.write(self.style.MIGRATE_HEADING('\n--- Students ---'))
        for s in STUDENTS:
            user, created = User.objects.get_or_create(
                username=s['email'],
                defaults={
                    'email': s['email'],
                    'first_name': s['first'],
                    'last_name': s['last'],
                    'role': 'student',
                }
            )
            if created:
                user.set_password(s['password'])
                user.save()

            Student.objects.get_or_create(
                enrollment_no=s['enrollment'],
                defaults={
                    'user': user,
                    'department': dept_map[s['dept']],
                    'semester': 6,
                    'section': 'A',
                }
            )
            status = 'created' if created else 'exists'
            self.stdout.write(f"  [{status}] {s['first']} {s['last']} ({s['enrollment']}) — {s['dept']}")

        # 3. Faculty
        self.stdout.write(self.style.MIGRATE_HEADING('\n--- Faculty ---'))
        for f in FACULTY:
            user, created = User.objects.get_or_create(
                username=f['email'],
                defaults={
                    'email': f['email'],
                    'first_name': f['first'],
                    'last_name': f['last'],
                    'role': 'faculty',
                }
            )
            if created:
                user.set_password(f['password'])
                user.save()

            Faculty.objects.get_or_create(
                faculty_id=f['fid'],
                defaults={
                    'user': user,
                    'department': dept_map[f['dept']],
                    'designation': f['designation'],
                }
            )
            status = 'created' if created else 'exists'
            self.stdout.write(f"  [{status}] {f['first']} {f['last']} ({f['fid']}) — {f['dept']}")

        # 4. Demo / Admin accounts
        self.stdout.write(self.style.MIGRATE_HEADING('\n--- Demo & Admin Accounts ---'))
        for d in DEMO_ACCOUNTS:
            user, created = User.objects.get_or_create(
                username=d['email'],
                defaults={
                    'email': d['email'],
                    'first_name': d['first'],
                    'last_name': d['last'],
                    'role': d['role'],
                    'is_staff': d.get('is_staff', False),
                    'is_superuser': d.get('is_superuser', False),
                }
            )
            if created:
                user.set_password(d['password'])
                user.save()

            # Create Parent profile for demo parent
            if d['role'] == 'parent':
                parent_obj, _ = Parent.objects.get_or_create(user=user)
                # Link demo parent to the demo student (Udit Rathore - 2022AIML004)
                try:
                    demo_student = Student.objects.get(enrollment_no='2022AIML004')
                    demo_student.parent = parent_obj
                    demo_student.save()
                except Student.DoesNotExist:
                    pass

            # Create Student profile for demo student
            if d['role'] == 'student':
                Student.objects.get_or_create(
                    user=user,
                    defaults={
                        'enrollment_no': '2022AIML045',
                        'department': dept_map['AIML'],
                        'semester': 6,
                        'section': 'A',
                    }
                )

            status = 'created' if created else 'exists'
            self.stdout.write(f"  [{status}] {d['email']} ({d['role']})")

        self.stdout.write(self.style.SUCCESS('\n✅ Seed complete!'))
        self.stdout.write('   Run: python manage.py runserver')
        self.stdout.write('   API: http://127.0.0.1:8000/api/auth/login/')
