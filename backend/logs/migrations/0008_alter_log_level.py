# Generated by Django 4.1.7 on 2023-03-25 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0007_logfile_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='level',
            field=models.IntegerField(choices=[(0, 'Неназначен'), (1, 'КРИТИЧЕСКИЙ'), (2, 'ОШИБКА'), (3, 'ПРЕДУПРЕЖДЕНИЕ'), (4, 'ИНФОРМАТИВНЫЙ')]),
        ),
    ]
