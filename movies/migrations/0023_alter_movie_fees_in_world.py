# Generated by Django 3.2.8 on 2022-01-27 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0022_auto_20220127_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='fees_in_world',
            field=models.PositiveIntegerField(default=0, help_text='указывать сумму в долларах', verbose_name='Сборы в мире'),
        ),
    ]
