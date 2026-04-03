from django.db import models
from accounts.models import User, StudentProfile

DAY_CHOICES = [
    ('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'),
    ('THU', 'Thursday'), ('FRI', 'Friday'),
]

TYPE_CHOICES = [
    ('theory',     'Theory'),
    ('practical',  'Practical'),
    ('project',    'Project'),
]

STATUS_CHOICES = [
    ('present', 'Present'),
    ('absent',  'Absent'),
    ('late',    'Late'),
]

# All subjects from the AIML 6th sem timetable
SUBJECT_CHOICES = [
    ('IP',      'Image & Video Processing'),
    ('CC',      'Cloud Computing'),
    ('PDP',     'PDP'),
    ('CN',      'Computer Networks'),
    ('TOC',     'Theory of Computation'),
    ('MP',      'Minor Project'),
    ('IP_LAB',  'Practical — Image & Video Processing'),
    ('CC_LAB',  'Practical — Cloud Computing'),
    ('CN_LAB',  'Practical — Computer Networks'),
    ('TOC_LAB', 'Practical — Theory of Computation'),
    ('APT',     'Aptitude'),
    ('CP',      'Competitive Programming'),
]

BATCH_CHOICES = [
    ('ALL', 'All Students'),
    ('B1',  'Batch 1'),
    ('B2',  'Batch 2'),
]


class TimetableSlot(models.Model):
    """Represents one recurring slot in the weekly timetable."""
    day         = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time  = models.TimeField()
    end_time    = models.TimeField()
    subject     = models.CharField(max_length=10, choices=SUBJECT_CHOICES)
    type        = models.CharField(max_length=10, choices=TYPE_CHOICES, default='theory')
    batch       = models.CharField(max_length=3, choices=BATCH_CHOICES, default='ALL')
    faculty     = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        limit_choices_to={'role': 'faculty'}
    )
    room        = models.CharField(max_length=20, default='Room 28')

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.get_day_display()} {self.start_time} — {self.get_subject_display()} ({self.batch})"


class AttendanceSession(models.Model):
    """One actual class session on a specific date."""
    slot        = models.ForeignKey(TimetableSlot, on_delete=models.CASCADE, related_name='sessions')
    date        = models.DateField()
    marked_by   = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        limit_choices_to={'role': 'faculty'}, related_name='marked_sessions'
    )
    is_finalized = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('slot', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} — {self.slot.get_subject_display()}"


class AttendanceRecord(models.Model):
    """Individual student attendance for one session."""
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_records')
    status  = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')

    class Meta:
        unique_together = ('session', 'student')

    def __str__(self):
        return f"{self.student} — {self.session} — {self.status}"


class AttendanceSummary(models.Model):
    """Cached summary per student per subject for quick display."""
    student         = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='summaries')
    subject         = models.CharField(max_length=10, choices=SUBJECT_CHOICES)
    total_classes   = models.PositiveIntegerField(default=0)
    present_count   = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('student', 'subject')

    @property
    def percentage(self):
        if self.total_classes == 0:
            return 0
        return round((self.present_count / self.total_classes) * 100, 1)

    @property
    def is_shortage(self):
        return self.percentage < 75

    def __str__(self):
        return f"{self.student} — {self.subject} — {self.percentage}%"
