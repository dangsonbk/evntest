# Generated by Django 3.1 on 2021-06-28 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20210628_1432'),
        ('multichoice', '0004_upload_imported'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='imported',
            field=models.BooleanField(default=False, verbose_name='Đã nạp câu hỏi'),
        ),
    ]