"""
Management command: python manage.py seed_parents

Seeds parent accounts linked to their children.
Safe to run multiple times — uses get_or_create.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Parent, Student

User = get_user_model()

PARENTS = [
    # AIML
    {'email':'rajesh.kanojiya@gmail.com',    'password':'rajesh@123',   'first':'Rajesh',   'last':'Kanojiya',    'child':'2022AIML001'},
    {'email':'sunita.rathore@gmail.com',     'password':'sunita@123',   'first':'Sunita',   'last':'Rathore',     'child':'2022AIML002'},
    {'email':'arvind.punase@gmail.com',      'password':'arvind@123',   'first':'Arvind',   'last':'Punase',      'child':'2022AIML003'},
    {'email':'mahesh.rathore@gmail.com',     'password':'mahesh@123',   'first':'Mahesh',   'last':'Rathore',     'child':'2022AIML004'},
    {'email':'dinesh.chikhalikar@gmail.com', 'password':'dinesh@123',   'first':'Dinesh',   'last':'Chikhalikar', 'child':'2022AIML005'},
    {'email':'rekha.upadhya@gmail.com',      'password':'rekha@123',    'first':'Rekha',    'last':'Upadhya',     'child':'2022AIML006'},
    {'email':'ramesh.jain@gmail.com',        'password':'ramesh@123',   'first':'Ramesh',   'last':'Jain',        'child':'2022AIML007'},
    {'email':'geeta.malviya@gmail.com',      'password':'geeta@123',    'first':'Geeta',    'last':'Malviya',     'child':'2022AIML008'},
    {'email':'suresh.adlak@gmail.com',       'password':'suresh@123',   'first':'Suresh',   'last':'Adlak',       'child':'2022AIML009'},
    {'email':'kamlesh.joshi@gmail.com',      'password':'kamlesh@123',  'first':'Kamlesh',  'last':'Joshi',       'child':'2022AIML010'},
    # CS
    {'email':'vikram.sharma@gmail.com',      'password':'vikram@123',   'first':'Vikram',   'last':'Sharma',      'child':'2022CS001'},
    {'email':'priya.gupta@gmail.com',        'password':'priya@123',    'first':'Priya',    'last':'Gupta',       'child':'2022CS002'},
    {'email':'anil.pardeshi@gmail.com',      'password':'anil@123',     'first':'Anil',     'last':'Pardeshi',    'child':'2022CS003'},
    {'email':'rajani.tiwari@gmail.com',      'password':'rajani@123',   'first':'Rajani',   'last':'Tiwari',      'child':'2022CS004'},
    {'email':'sanjay.patel@gmail.com',       'password':'sanjay@123',   'first':'Sanjay',   'last':'Patel',       'child':'2022CS005'},
    # IT
    {'email':'mohan.tolani@gmail.com',       'password':'mohan@123',    'first':'Mohan',    'last':'Tolani',      'child':'2022IT001'},
    {'email':'lata.choure@gmail.com',        'password':'lata@123',     'first':'Lata',     'last':'Choure',      'child':'2022IT002'},
    {'email':'deepak.paliwal@gmail.com',     'password':'deepak@123',   'first':'Deepak',   'last':'Paliwal',     'child':'2022IT003'},
    {'email':'meena.shukla@gmail.com',       'password':'meena@123',    'first':'Meena',    'last':'Shukla',      'child':'2022IT008'},
    {'email':'sunil.tiwari@gmail.com',       'password':'sunil@123',    'first':'Sunil',    'last':'Tiwari',      'child':'2022IT009'},
    # ME
    {'email':'rajeev.jaiswal@gmail.com',     'password':'rajeev@123',   'first':'Rajeev',   'last':'Jaiswal',     'child':'2022ME001'},
    {'email':'kavita.chouhan@gmail.com',     'password':'kavita@123',   'first':'Kavita',   'last':'Chouhan',     'child':'2022ME002'},
    {'email':'hemant.prajapati@gmail.com',   'password':'hemant@123',   'first':'Hemant',   'last':'Prajapati',   'child':'2022ME003'},
    {'email':'anita.verma@gmail.com',        'password':'anita@123',    'first':'Anita',    'last':'Verma',       'child':'2022ME004'},
    {'email':'raju.yadav@gmail.com',         'password':'raju@123',     'first':'Raju',     'last':'Yadav',       'child':'2022ME007'},
]


class Command(BaseCommand):
    help = 'Seed parent accounts and link them to their children'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('=== Seeding Parents ==='))

        for p in PARENTS:
            # Create parent user
            user, created = User.objects.get_or_create(
                username=p['email'],
                defaults={
                    'email':      p['email'],
                    'first_name': p['first'],
                    'last_name':  p['last'],
                    'role':       'parent',
                }
            )
            if created:
                user.set_password(p['password'])
                user.save()

            # Create Parent profile
            parent_obj, _ = Parent.objects.get_or_create(user=user)

            # Link to child
            try:
                student = Student.objects.get(enrollment_no=p['child'])
                student.parent = parent_obj
                student.save()
                child_name = student.user.get_full_name()
            except Student.DoesNotExist:
                child_name = f'NOT FOUND ({p["child"]})'

            status = 'created' if created else 'exists'
            self.stdout.write(
                f'  [{status}] {p["first"]} {p["last"]} → child: {child_name}'
            )

        self.stdout.write(self.style.SUCCESS('\n✅ Parents seeded!'))
        self.stdout.write('   Login: parent email + password (e.g. rajesh.kanojiya@gmail.com / rajesh@123)')
