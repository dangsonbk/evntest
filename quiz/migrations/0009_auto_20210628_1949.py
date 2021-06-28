# Generated by Django 3.0.7 on 2021-06-28 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_auto_20210628_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Họ tên'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='branch',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Chi nhánh'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Ngày sinh'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('0', 'Male'), ('1', 'Female')], default='0', max_length=1, verbose_name='Giới tính'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='title',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Chức danh'),
        ),
    ]
