# Generated by Django 3.2.7 on 2021-10-05 18:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_delete_articlestatistic'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('views', models.IntegerField(default=0, verbose_name='Просмотры')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
            options={
                'db_table': 'ArticleStatistic',
            },
        ),
    ]
