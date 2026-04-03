from django.db import models
from accounts.models import User

SUBJECT_CHOICES = [
    ('CN',  'Computer Networks'),
    ('TOC', 'Theory of Computation'),
    ('CC',  'Cloud Computing'),
    ('IP',  'Image & Video Processing'),
    ('TOC_LAB', 'Practical — Theory of Computation'),
    ('IP_LAB',  'Practical — Image & Video Processing'),
    ('CN_LAB',  'Practical — Computer Networks'),
    ('MP',  'Minor Project'),
    ('PDP', 'PDP'),
    ('CP',  'Competitive Programming'),
]


class Note(models.Model):
    title      = models.CharField(max_length=200)
    subject    = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    file       = models.FileField(upload_to='notes/%Y/%m/')
    uploaded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        limit_choices_to={'role': 'faculty'}
    )
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.get_subject_display()} — {self.title}"
