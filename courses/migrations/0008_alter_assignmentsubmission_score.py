# Generated by Django 5.1.7 on 2025-04-09 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_assignmentsubmission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='score',
            field=models.PositiveIntegerField(help_text='Score given by the teacher', null=True),
        ),
    ]
