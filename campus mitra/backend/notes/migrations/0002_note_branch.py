from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='branch',
            field=models.CharField(
                choices=[
                    ('AIML', 'AI & Machine Learning'),
                    ('ME',   'Mechanical Engineering'),
                    ('CS',   'Computer Science'),
                    ('ALL',  'All Branches'),
                ],
                default='ALL',
                max_length=10,
            ),
        ),
    ]
