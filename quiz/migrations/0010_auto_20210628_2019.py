# Generated by Django 3.0.7 on 2021-06-28 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_auto_20210628_1949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': 'Phòng ban', 'verbose_name_plural': 'Phòng ban'},
        ),
        migrations.AddField(
            model_name='department',
            name='categories',
            field=models.ManyToManyField(blank=True, to='quiz.Category', verbose_name='Phân loại đề thi'),
        ),
        migrations.AlterField(
            model_name='department',
            name='department',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Phòng ban'),
        ),
    ]
