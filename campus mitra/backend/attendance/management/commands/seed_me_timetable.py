from django.core.management.base import BaseCommand
from datetime import time
from attendance.models import TimetableSlot
from accounts.models import User


class Command(BaseCommand):
    help = 'Seed ME 6th sem timetable slots (Class ME-3, Room 30)'

    def get_faculty(self, first_name):
        return User.objects.filter(role='faculty', first_name__iexact=first_name).first()

    def handle(self, *args, **kwargs):
        TimetableSlot.objects.filter(branch='ME').delete()

        SV  = self.get_faculty('Saurabh')    # Machine Component Design
        RM  = self.get_faculty('Rahul')       # CAD Lab
        UB  = self.get_faculty('Umesh')       # Renewable Energy Technology
        DK  = self.get_faculty('Devendra')    # RDBMS Lab
        DS  = self.get_faculty('Dushyant')    # Thermal Engineering
        AB  = self.get_faculty('Abhishek')    # Aptitude

        slots = [
            # MONDAY
            ('MON', time(9,10),  time(10,10), 'MCD',      'theory',    'ALL', SV,  'Room 30'),
            ('MON', time(10,10), time(11,0),  'TE',       'theory',    'ALL', DS,  'Room 30'),
            ('MON', time(11,0),  time(11,50), 'RET',      'theory',    'ALL', UB,  'Room 30'),
            ('MON', time(11,50), time(12,40), 'RDBMS',    'theory',    'ALL', DK,  'Room 30'),
            ('MON', time(13,30), time(15,10), 'CAD_LAB',  'practical', 'B1',  RM,  'CAD Lab'),
            ('MON', time(13,30), time(15,10), 'CAD_LAB',  'practical', 'B2',  RM,  'CAD Lab'),

            # TUESDAY
            ('TUE', time(9,10),  time(11,0),  'APT_ME',   'theory',    'ALL', AB,  'Room 30'),
            ('TUE', time(11,0),  time(11,50), 'MCD',      'theory',    'ALL', SV,  'Room 30'),
            ('TUE', time(11,50), time(12,40), 'TE',       'theory',    'ALL', DS,  'Room 30'),
            ('TUE', time(13,30), time(15,10), 'RDBMS_LAB','practical', 'B1',  DK,  'Computer Lab'),
            ('TUE', time(13,30), time(15,10), 'RDBMS_LAB','practical', 'B2',  DK,  'Computer Lab'),

            # WEDNESDAY
            ('WED', time(9,10),  time(10,10), 'RET',      'theory',    'ALL', UB,  'Room 30'),
            ('WED', time(10,10), time(11,0),  'MCD',      'theory',    'ALL', SV,  'Room 30'),
            ('WED', time(11,0),  time(11,50), 'RDBMS',    'theory',    'ALL', DK,  'Room 30'),
            ('WED', time(11,50), time(12,40), 'TE',       'theory',    'ALL', DS,  'Room 30'),
            ('WED', time(13,30), time(15,10), 'CAD_LAB',  'practical', 'B2',  RM,  'CAD Lab'),

            # THURSDAY
            ('THU', time(9,10),  time(10,10), 'TE',       'theory',    'ALL', DS,  'Room 30'),
            ('THU', time(10,10), time(11,0),  'RET',      'theory',    'ALL', UB,  'Room 30'),
            ('THU', time(11,0),  time(12,40), 'MCD_LAB',  'practical', 'B1',  SV,  'Workshop'),
            ('THU', time(11,0),  time(12,40), 'MCD_LAB',  'practical', 'B2',  SV,  'Workshop'),
            ('THU', time(13,30), time(14,20), 'RDBMS',    'theory',    'ALL', DK,  'Room 30'),
            ('THU', time(14,20), time(15,10), 'MCD',      'theory',    'ALL', SV,  'Room 30'),

            # FRIDAY
            ('FRI', time(9,10),  time(11,0),  'APT_ME',   'theory',    'ALL', AB,  'Room 30'),
            ('FRI', time(11,0),  time(11,50), 'RET',      'theory',    'ALL', UB,  'Room 30'),
            ('FRI', time(11,50), time(12,40), 'MCD',      'theory',    'ALL', SV,  'Room 30'),
            ('FRI', time(13,30), time(15,10), 'RDBMS_LAB','practical', 'B2',  DK,  'Computer Lab'),
            ('FRI', time(15,10), time(16,0),  'TE',       'theory',    'ALL', DS,  'Room 30'),
        ]

        count = 0
        for day, start, end, subj, stype, batch, fac, room in slots:
            slot = TimetableSlot.objects.create(
                day=day, start_time=start, end_time=end,
                subject=subj, type=stype, batch=batch,
                branch='ME', faculty=fac, room=room
            )
            self.stdout.write(f'  {slot}')
            count += 1

        self.stdout.write(self.style.SUCCESS(f'\nME timetable seeded — {count} slots created!'))
