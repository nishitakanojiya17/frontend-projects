from django.core.management.base import BaseCommand
from accounts.models import User, StudentProfile, ParentProfile

# Parent name mapped to student enroll_no
# Pattern: parent username = parent.<student_first>.<student_last>@iist.ac.in
# Password = parent@<student_first_lower>123

PARENTS = [
    # (parent_first, parent_last, student_enroll)
    ('Praveen',    'Kanojiya',    '2022AIML001'),
    ('Suresh',    'Rathore',     '2022AIML002'),
    ('Mahesh',    'Punase',      '2022AIML003'),
    ('Dinesh',    'Rathore',     '2022AIML004'),
    ('Ramesh',    'Chikhalikar', '2022AIML005'),
    ('Naresh',    'Upadhya',     '2022AIML006'),
    ('Kamlesh',   'Jain',        '2022AIML007'),
    ('Viresh',    'Malviya',     '2022AIML008'),
    ('Ganesh',    'Adlak',       '2022AIML009'),
    ('Mukesh',    'Joshi',       '2022AIMPS C:\Users\Nishita\OneDrive\Desktop\frontend-projects> cd "campus mitra/backend"
PS C:\Users\Nishita\OneDrive\Desktop\frontend-projects\campus mitra\backend> python manage.py shell -c "
>> from accounts.models import User, ParentProfile
>> parents = ParentProfile.objects.select_related('user', 'child__user').all()
>> for p in parents:
>>     print(f'{p.user.get_full_name()} | {p.user.username} | child: {p.child.user.get_full_name() if p.child else \"None\"}')
>> "
20 objects imported automatically (use -v 2 for details).

Traceback (most recent call last):
  File "C:\Users\Nishita\OneDrive\Desktop\frontend-projects\campus mitra\backend\manage.py", line 30, in <module>
    main()
  File "C:\Users\Nishita\OneDrive\Desktop\frontend-projects\campus mitra\backend\manage.py", line 26, in main
    execute_from_command_line(sys.argv)
  File "C:\Users\Nishita\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\django\core\management\__init__.py", line 443, in execute_from_command_line
    utility.execute()
  File "C:\Users\Nishita\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\django\core\management\__init__.py", line 437, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "C:\Users\Nishita\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\django\core\management\base.py", line 420, in run_from_argv
    self.execute(*args, **cmd_options)
  File "C:\Users\Nishita\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\django\core\management\base.py", line 464, in execute
    output = self.handle(*args, **options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Nishita\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\django\core\management\commands\shell.py", line 261, in handle
    exec(options["command"], {**globals(), **self.get_namespace(**options)})
  File "<string>", line 5
    print(f'{p.user.get_full_name()} | {p.user.username} | child: {p.child.user.get_full_name() if p.child else " None\}')
                                                                                                
                ^
SyntaxError: unterminated string literal (detected at line 5)
PS C:\Users\Nishita\OneDrive\Desktop\frontend-projects\campus mitra\backend> L010'),
    ('Rakesh',    'Jain',        '2022AIML011'),
    ('Umesh',     'Singh',       '2022AIML012'),
    ('Lokesh',    'Mahajan',     '2022AIML013'),
    ('Hitesh',    'Prajapat',    '2022AIML014'),
    ('Yogesh',    'Rassay',      '2022AIML015'),
    ('Nilesh',    'Malakar',     '2022AIML016'),
    ('Devesh',    'Pawar',       '2022AIML017'),
    ('Brijesh',   'Pawar',       '2022AIML018'),
    ('Santosh',   'Singh',       '2022AIML019'),
    ('Prakash',   'Singh',       '2022AIML020'),
]


class Command(BaseCommand):
    help = 'Seed parent accounts linked to 20 AIML students'

    def handle(self, *args, **kwargs):
        for first, last, enroll in PARENTS:
            username = f"parent.{first.lower()}.{last.lower()}@iist.ac.in"
            password = f"parent@{first.lower()}123"

            student = StudentProfile.objects.filter(enroll_no=enroll).first()
            if not student:
                self.stdout.write(self.style.WARNING(
                    f'Student {enroll} not found — run seed_students first.'
                ))
                continue

            if User.objects.filter(username=username).exists():
                self.stdout.write(f'Already exists: {username}')
                continue

            user = User.objects.create_user(
                username=username,
                email=username,
                password=password,
                first_name=first,
                last_name=last,
                role='parent'
            )
            ParentProfile.objects.create(user=user, child=student)

            self.stdout.write(self.style.SUCCESS(
                f'Created: {first} {last} | {username} | pwd: {password} | child: {enroll}'
            ))

        self.stdout.write(self.style.SUCCESS('\nAll 20 parent accounts created!'))
