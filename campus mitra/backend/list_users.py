import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmitra.settings')
django.setup()

from accounts.models import User, ParentProfile

print("\n--- PARENTS ---")
for p in ParentProfile.objects.select_related('user', 'child__user').all():
    child_name = p.child.user.get_full_name() if p.child else 'None'
    child_enroll = p.child.enroll_no if p.child else 'None'
    print(f"{p.user.get_full_name():<25} | {p.user.username:<45} | child: {child_name} ({child_enroll})")

print("\n--- ALL USERS ---")
for u in User.objects.all().order_by('role'):
    print(f"{u.role:<10} | {u.get_full_name():<25} | {u.username}")
