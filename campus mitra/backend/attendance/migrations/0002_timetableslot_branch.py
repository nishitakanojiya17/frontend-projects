from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetableslot',
            name='branch',
            field=models.CharField(
                choices=[
                    ('AIML', 'AI & Machine Learning'),
                    ('CS',   'Computer Science'),
                    ('ME',   'Mechanical Engineering'),
                ],
                default='AIML',
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name='timetableslot',
            name='subject',
            field=models.CharField(max_length=15, choices=[
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
            ]),
        ),
        migrations.AlterField(
            model_name='attendancesummary',
            name='subject',
            field=models.CharField(max_length=15, choices=[
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
            ]),
        ),
    ]
