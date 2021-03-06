# Generated by Django 3.0.7 on 2021-07-29 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20210729_1936'),
        ('multichoice', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'Câu trả lời', 'verbose_name_plural': 'Câu trả lời'},
        ),
        migrations.AlterModelOptions(
            name='mcquestion',
            options={'verbose_name': 'Câu hỏi nhiều lựa chọn', 'verbose_name_plural': 'Câu hỏi nhiều lựa chọn'},
        ),
        migrations.AlterField(
            model_name='answer',
            name='content',
            field=models.CharField(help_text='Câu trả lời', max_length=1000, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='correct',
            field=models.BooleanField(default=False, help_text='Câu trả lời đúng', verbose_name='Correct'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='multichoice.MCQuestion', verbose_name='Câu hỏi'),
        ),
        migrations.AlterField(
            model_name='mcquestion',
            name='answer_order',
            field=models.CharField(blank=True, choices=[('content', 'Nội dung'), ('random', 'Ngẫu nhiên'), ('none', 'Không chọn')], help_text='The order in which multichoice answer options are displayed to the user', max_length=30, null=True, verbose_name='Thứ tự câu trả lời'),
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_file', models.FileField(upload_to='sample_quiz')),
                ('imported', models.BooleanField(default=False, verbose_name='Đã nạp câu hỏi')),
                ('grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Grade', verbose_name='Bậc thợ')),
            ],
            options={
                'verbose_name': 'Tải lên danh sách câu hỏi',
                'verbose_name_plural': 'Tải lên danh sách câu hỏi',
            },
        ),
    ]
