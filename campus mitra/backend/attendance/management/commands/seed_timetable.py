from django.core.management.base import BaseCommand
from datetime import time
from attendance.models import TimetableSlot
from accounts.models import User


class Command(BaseCommand):
    help = 'Seed AIML 6th sem timetable slots'

    def handle(self, *args, **kwargs):
        def faculty(name):
            first = name.split('.')[0].strip()
            try:
                return User.objects.filter(role='faculty', first_name__iexact=first).first()
            except Exception:
                return None

        TimetableSlot.objects.all().delete()

        slots = [
            # MONDAY
            ('MON', time(9,10),  time(10,10), 'IP',      'theory',    'ALL', 'Ratnesh',   'Room 28'),
            ('MON', time(10,10), time(11,0),  'CC',      'theory',    'ALL', 'Nishant',   'Room 28'),
            ('MON', time(11,0),  time(11,50), 'PDP',     'theory',    'ALL', 'Jaya',      'Room 28'),
            ('MON', time(11,50), time(12,40), 'CN',      'theory',    'ALL', 'Smita',     'Room 28'),
            ('MON', time(13,30), time(14,20), 'MP',      'project',   'ALL', 'Sukruti',   'Room 28'),
            ('MON', time(15,10), time(16,0),  'TOC',     'theory',    'ALL', 'Aatish',    'Room 28'),

            # TUESDAY
            ('TUE', time(9,10),  time(10,10), 'IP',      'theory',    'ALL', 'Ratnesh',   'Room 28'),
            ('TUE', time(10,10), time(11,0),  'CC',      'theory',    'ALL', 'Nishant',   'Room 28'),
            ('TUE', time(11,0),  time(11,50), 'TOC',     'theory',    'ALL', 'Aatish',    'Room 28'),
            ('TUE', time(11,50), time(12,40), 'PDP',     'theory',    'ALL', 'Jaya',      'Room 28'),
            ('TUE', time(13,30), time(14,20), 'CN',      'theory',    'ALL', 'Smita',     'Room 28'),
            ('TUE', time(14,20), time(16,0),  'CP',      'practical', 'ALL', 'Shivani',   'Lab'),

            # WEDNESDAY
            ('WED', time(9,10),  time(11,0),  'APT',     'theory',    'ALL', 'Abhishek',  'Room 28'),
            ('WED', time(11,0),  time(11,50), 'CN',      'theory',    'ALL', 'Smita',     'Room 28'),
            ('WED', time(11,50), time(12,40), 'TOC',     'theory',    'ALL', 'Aatish',    'Room 28'),
            ('WED', time(13,30), time(15,10), 'CN_LAB',  'practical', 'B1',  'Smita',     'IT Lab'),
            ('WED', time(13,30), time(15,10), 'TOC_LAB', 'practical', 'B2',  'Aatish',    'IT Lab'),
            ('WED', time(15,10), time(16,0),  'IP',      'theory',    'ALL', 'Ratnesh',   'Room 28'),

            # THURSDAY
            ('THU', time(9,10),  time(11,0),  'IP_LAB',  'practical', 'B1',  'Ratnesh',   'IT Lab'),
            ('THU', time(9,10),  time(11,0),  'CC_LAB',  'practical', 'B2',  'Nishant',   'IT Lab'),
            ('THU', time(11,0),  time(12,40), 'CN_LAB',  'practical', 'B2',  'Smita',     'IT Lab'),
            ('THU', time(11,0),  time(12,40), 'TOC_LAB', 'practical', 'B1',  'Aatish',    'IT Lab'),
            ('THU', time(13,30), time(14,20), 'CC',      'theory',    'ALL', 'Nishant',   'Room 28'),
            ('THU', time(14,20), time(15,10), 'PDP',     'theory',    'ALL', 'Jaya',      'Room 28'),
            ('THU', time(15,10), time(16,0),  'TOC',     'theory',    'ALL', 'Aatish',    'Room 28'),

            # FRIDAY
            ('FRI', time(9,10),  time(11,0),  'IP_LAB',  'practical', 'B2',  'Ratnesh',   'IT Lab'),
            ('FRI', time(9,10),  time(11,0),  'CC_LAB',  'practical', 'B1',  'Nishant',   'IT Lab'),
            ('FRI', time(11,0),  time(11,50), 'CN',      'theory',    'ALL', 'Smita',     'Room 28'),
            ('FRI', time(11,50), time(12,40), 'IP',      'theory',    'ALL', 'Ratnesh',   'Room 28'),
            ('FRI', time(14,20), time(16,0),  'CP',      'practical', 'ALL', 'Shivani',   'Lab'),
            ('FRI', time(15,10), time(16,0),  'APT',     'theory',    'ALL', 'Abhishek',  'Room 28'),
        ]

        for day, start, end, subj, stype, batch, fname, room in slots:
            f = User.objects.filter(role='faculty', first_name__iexact=fname).first()
            slot = TimetableSlot.objects.create(
                day=day, start_time=start, end_time=end,
                subject=subj, type=stype, batch=batch,
                faculty=f, room=room
            )
            self.stdout.write(f'Created: {slot}')

        self.stdout.write(self.style.SUCCESS(f'\nTimetable seeded — {len(slots)} slots created!'))
