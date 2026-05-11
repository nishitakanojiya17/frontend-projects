from django.core.management.base import BaseCommand
from datetime import time
from attendance.models import TimetableSlot
from accounts.models import User


class Command(BaseCommand):
    help = 'Seed CS 6th sem timetable slots (Class CS-3, Room 27)'

    def get_faculty(self, first_name):
        return User.objects.filter(role='faculty', first_name__iexact=first_name).first()

    def handle(self, *args, **kwargs):
        # Remove existing CS slots only
        TimetableSlot.objects.filter(branch='CS').delete()

        # Faculty lookup by first name
        RTG = self.get_faculty('Reetu')      # ML
        RG  = self.get_faculty('Rati')       # CN
        SP  = self.get_faculty('Shreyas')    # CD
        DK  = self.get_faculty('Devendra')   # PM
        MT  = self.get_faculty('Muskan')     # DAL
        PS  = self.get_faculty('Purva')      # SDL / Minor Project
        GS  = self.get_faculty('Gourav')     # PDP
        AB  = self.get_faculty('Abhishek')   # APTT
        GP  = self.get_faculty('Ganesh')     # SIG-CP

        slots = [
            # day, start, end, subject, type, batch, faculty, room

            # MONDAY
            ('MON', time(9,10),  time(11,0),  'SIG_CP',    'theory',    'ALL', GP,  'Room 27'),
            ('MON', time(11,0),  time(11,50), 'CD',        'theory',    'ALL', SP,  'Room 27'),
            ('MON', time(11,50), time(12,40), 'CN_CS',     'theory',    'ALL', RG,  'Room 27'),
            ('MON', time(13,30), time(14,20), 'PDP',       'theory',    'ALL', GS,  'Room 27'),
            ('MON', time(14,20), time(16,0),  'DAL_LAB',   'practical', 'B2', MT,  'Lab'),
            ('MON', time(14,20), time(16,0),  'SDL_LAB',   'practical', 'B1', PS,  'Lab'),

            # TUESDAY
            ('TUE', time(9,10),  time(11,0),  'APTT',      'theory',    'ALL', AB,  'Room 27'),
            ('TUE', time(11,0),  time(13,0),  'DAL_LAB',   'practical', 'B1', MT,  'Lab'),
            ('TUE', time(11,0),  time(13,0),  'SDL_LAB',   'practical', 'B2', PS,  'Lab'),
            ('TUE', time(13,30), time(14,20), 'ML',        'theory',    'ALL', RTG, 'Room 27'),
            ('TUE', time(14,20), time(16,0),  'ML_LAB',    'practical', 'B2', RTG, 'Lab'),
            ('TUE', time(14,20), time(16,0),  'CN_CS_LAB', 'practical', 'B1', RG,  'Lab'),

            # WEDNESDAY
            ('WED', time(9,10),  time(10,10), 'CN_CS',     'theory',    'ALL', RG,  'Room 27'),
            ('WED', time(10,10), time(11,0),  'CD',        'theory',    'ALL', SP,  'Room 27'),
            ('WED', time(11,0),  time(13,0),  'ML_LAB',    'practical', 'B1', RTG, 'Lab'),
            ('WED', time(11,0),  time(13,0),  'CN_CS_LAB', 'practical', 'B2', RG,  'Lab'),
            ('WED', time(13,30), time(14,20), 'ML',        'theory',    'ALL', RTG, 'Room 27'),
            ('WED', time(14,20), time(15,10), 'PM',        'theory',    'ALL', DK,  'Room 27'),

            # THURSDAY
            ('THU', time(9,10),  time(10,10), 'PDP',       'theory',    'ALL', GS,  'Room 27'),
            ('THU', time(10,10), time(11,0),  'CD',        'theory',    'ALL', SP,  'Room 27'),
            ('THU', time(11,0),  time(12,40), 'SIG_CP',    'theory',    'ALL', GP,  'Room 27'),
            ('THU', time(13,30), time(14,20), 'CN_CS',     'theory',    'ALL', RG,  'Room 27'),
            ('THU', time(14,20), time(15,10), 'ML',        'theory',    'ALL', RTG, 'Room 27'),
            ('THU', time(15,10), time(16,0),  'PM',        'theory',    'ALL', DK,  'Room 27'),

            # FRIDAY
            ('FRI', time(9,10),  time(11,0),  'CS_MP',     'project',   'ALL', PS,  'Room 27'),
            ('FRI', time(11,0),  time(11,50), 'PDP',       'theory',    'ALL', GS,  'Room 27'),
            ('FRI', time(11,50), time(12,40), 'ML',        'theory',    'ALL', RTG, 'Room 27'),
            ('FRI', time(13,30), time(14,20), 'PM',        'theory',    'ALL', DK,  'Room 27'),
            ('FRI', time(14,20), time(15,10), 'CN_CS',     'theory',    'ALL', RG,  'Room 27'),
            ('FRI', time(15,10), time(16,0),  'CD',        'theory',    'ALL', SP,  'Room 27'),
        ]

        count = 0
        for day, start, end, subj, stype, batch, fac, room in slots:
            slot = TimetableSlot.objects.create(
                day=day, start_time=start, end_time=end,
                subject=subj, type=stype, batch=batch,
                branch='CS', faculty=fac, room=room
            )
            self.stdout.write(f'  {slot}')
            count += 1

        self.stdout.write(self.style.SUCCESS(f'\nCS timetable seeded — {count} slots created!'))
