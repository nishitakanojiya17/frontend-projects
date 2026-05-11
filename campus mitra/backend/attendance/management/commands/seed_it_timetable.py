from django.core.management.base import BaseCommand
from datetime import time
from attendance.models import TimetableSlot
from accounts.models import User


class Command(BaseCommand):
    help = 'Seed IT 6th sem timetable slots (Class IT-3, Room 29)'

    def get_faculty(self, first_name):
        return User.objects.filter(role='faculty', first_name__iexact=first_name).first()

    def handle(self, *args, **kwargs):
        TimetableSlot.objects.filter(branch='IT').delete()

        SHM = self.get_faculty('Sheetal')    # CGMM (Sheetal Mandloi)
        DAS = self.get_faculty('Ankit')      # WMC
        RJ  = self.get_faculty('Rakesh')     # CD
        PSD = self.get_faculty('Puneet')     # SE
        SHD = self.get_faculty('Shreya')     # PP (Shreya Dubey)
        DK  = self.get_faculty('Devendra')   # AD
        RY  = self.get_faculty('Rupal')      # Minor Project
        MS  = self.get_faculty('Mohit')      # PDP
        AB  = self.get_faculty('Abhishek')   # APTT
        VZ  = self.get_faculty('Varsha')     # CP

        slots = [
            # day, start, end, subject, type, batch, faculty, room

            # MONDAY
            ('MON', time(10,0),  time(10,50), 'CD_IT',    'theory',    'ALL', RJ,  'Room 29'),
            ('MON', time(10,50), time(11,40), 'PDP_IT',   'theory',    'ALL', MS,  'Room 29'),
            ('MON', time(11,40), time(13,20), 'AND_LAB',  'practical', 'B2', SHD, 'Lab'),
            ('MON', time(11,40), time(13,20), 'AND_LAB',  'practical', 'B1', SHD, 'Lab'),
            ('MON', time(14,10), time(15,0),  'CGMM',     'theory',    'ALL', SHM, 'Room 29'),
            ('MON', time(15,0),  time(15,50), 'CGMM_LAB', 'practical', 'B1', SHM, 'Lab'),
            ('MON', time(15,0),  time(15,50), 'WMC_LAB',  'practical', 'B2', DAS, 'Lab'),
            ('MON', time(15,50), time(16,40), 'WMC_LAB',  'practical', 'B1', DAS, 'Lab'),

            # TUESDAY
            ('TUE', time(10,0),  time(11,40), 'APTT_IT',  'theory',    'ALL', AB,  'Room 29'),
            ('TUE', time(11,40), time(12,30), 'SE_IT',    'theory',    'ALL', PSD, 'Room 29'),
            ('TUE', time(12,30), time(13,20), 'PDP_IT',   'theory',    'ALL', MS,  'Room 29'),
            ('TUE', time(14,10), time(16,10), 'IT_MP',    'project',   'ALL', RY,  'Room 29'),
            ('TUE', time(15,50), time(16,40), 'WMC',      'theory',    'ALL', DAS, 'Room 29'),

            # WEDNESDAY
            ('WED', time(10,0),  time(11,40), 'AND_LAB',  'practical', 'B1', SHD, 'Lab'),
            ('WED', time(10,0),  time(11,40), 'AND_LAB',  'practical', 'B2', SHD, 'Lab'),
            ('WED', time(11,40), time(12,30), 'PDP_IT',   'theory',    'ALL', MS,  'Room 29'),
            ('WED', time(12,30), time(13,20), 'CD_IT',    'theory',    'ALL', RJ,  'Room 29'),
            ('WED', time(14,10), time(15,0),  'SE_IT',    'theory',    'ALL', PSD, 'Room 29'),
            ('WED', time(15,0),  time(15,50), 'CGMM',     'theory',    'ALL', SHM, 'Room 29'),
            ('WED', time(15,50), time(16,40), 'WMC',      'theory',    'ALL', DAS, 'Room 29'),

            # THURSDAY
            ('THU', time(10,0),  time(10,50), 'CGMM',     'theory',    'ALL', SHM, 'Room 29'),
            ('THU', time(10,50), time(11,40), 'WMC',      'theory',    'ALL', DAS, 'Room 29'),
            ('THU', time(11,40), time(13,20), 'CP_IT',    'theory',    'ALL', VZ,  'Room 29'),
            ('THU', time(14,10), time(15,0),  'SE_IT',    'theory',    'ALL', PSD, 'Room 29'),
            ('THU', time(15,0),  time(15,50), 'SE_IT',    'theory',    'ALL', PSD, 'Room 29'),
            ('THU', time(15,50), time(16,40), 'APTT_IT',  'theory',    'ALL', AB,  'Room 29'),

            # FRIDAY
            ('FRI', time(10,0),  time(10,50), 'WMC',      'theory',    'ALL', DAS, 'Room 29'),
            ('FRI', time(10,50), time(11,40), 'CD_IT',    'theory',    'ALL', RJ,  'Room 29'),
            ('FRI', time(11,40), time(13,20), 'CP_IT',    'theory',    'ALL', VZ,  'Room 29'),
            ('FRI', time(14,10), time(15,0),  'CGMM',     'theory',    'ALL', SHM, 'Room 29'),
            ('FRI', time(15,0),  time(15,50), 'CGMM_LAB', 'practical', 'B1', SHM, 'Lab'),
            ('FRI', time(15,0),  time(15,50), 'WMC_LAB',  'practical', 'B2', DAS, 'Lab'),
            ('FRI', time(15,50), time(16,40), 'CGMM_LAB', 'practical', 'B2', SHM, 'Lab'),
            ('FRI', time(15,50), time(16,40), 'WMC_LAB',  'practical', 'B1', DAS, 'Lab'),
        ]

        count = 0
        for day, start, end, subj, stype, batch, fac, room in slots:
            slot = TimetableSlot.objects.create(
                day=day, start_time=start, end_time=end,
                subject=subj, type=stype, batch=batch,
                branch='IT', faculty=fac, room=room
            )
            self.stdout.write(f'  {slot}')
            count += 1

        self.stdout.write(self.style.SUCCESS(f'\nIT timetable seeded — {count} slots created!'))
