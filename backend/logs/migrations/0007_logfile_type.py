# Generated by Django 4.1.7 on 2023-03-25 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0006_alter_log_options_alter_log_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='logfile',
            name='type',
            field=models.IntegerField(choices=[(0, 'Активность'), (1, 'Traceback')], default=0),
        ),
    ]
