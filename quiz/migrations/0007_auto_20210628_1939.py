# Generated by Django 3.0.7 on 2021-06-28 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20210628_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='depart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Department', verbose_name='Phòng ban'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='department',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]