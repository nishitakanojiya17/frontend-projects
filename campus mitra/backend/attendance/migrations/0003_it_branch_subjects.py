from django.db import migrations, models

ALL_SUBJECTS = [
    ('IP', 'Image & Video Processing'), ('CC', 'Cloud Computing'),
    ('PDP', 'PDP'), ('CN', 'Computer Networks'),
    ('TOC', 'Theory of Computation'), ('MP', 'Minor Project'),
    ('IP_LAB', 'Practical — Image & Video Processing'),
    ('CC_LAB', 'Practical — Cloud Computing'),
    ('CN_LAB', 'Practical — Computer Networks'),
    ('TOC_LAB', 'Practical — Theory of Computation'),
    ('APT', 'Aptitude'), ('CP', 'Competitive Programming'),
    ('ML', 'Machine Learning'), ('CN_CS', 'Computer Networks (CS)'),
    ('CD', 'Compiler Design'), ('PM', 'Project Management'),
    ('DAL', 'DAL'), ('SDL', 'SDL'), ('CS_MP', 'Minor Project (CS)'),
    ('SIG_CP', 'Competitive Programming (CS)'), ('APTT', 'Aptitude (CS)'),
    ('DAL_LAB', 'Practical — DAL'), ('SDL_LAB', 'Practical — SDL'),
    ('ML_LAB', 'Practical — ML'), ('CN_CS_LAB', 'Practical — CN (CS)'),
    ('CGMM', 'Computer Graphics & Multimedia'),
    ('WMC', 'Wireless & Mobile Computing'),
    ('CD_IT', 'Compiler Design (IT)'),
    ('SE_IT', 'Software Engineering (IT)'),
    ('PP', 'PP'), ('AD', 'Android Development'),
    ('IT_MP', 'Minor Project (IT)'),
    ('CP_IT', 'Competitive Programming (IT)'),
    ('APTT_IT', 'Aptitude (IT)'),
    ('PDP_IT', 'PDP (IT)'),
    ('AND_LAB', 'Practical — Android/Python'),
    ('CGMM_LAB', 'Practical — CGMM'),
    ('WMC_LAB', 'Practical — WMC'),
]

ALL_BRANCHES = [
    ('AIML', 'AI & Machine Learning'),
    ('CS', 'Computer Science'),
    ('IT', 'Information Technology'),
    ('ME', 'Mechanical Engineering'),
]


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_timetableslot_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetableslot',
            name='subject',
            field=models.CharField(max_length=15, choices=ALL_SUBJECTS),
        ),
        migrations.AlterField(
            model_name='timetableslot',
            name='branch',
            field=models.CharField(max_length=10, choices=ALL_BRANCHES, default='AIML'),
        ),
        migrations.AlterField(
            model_name='attendancesummary',
            name='subject',
            field=models.CharField(max_length=15, choices=ALL_SUBJECTS),
        ),
    ]
