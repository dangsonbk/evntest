# Generated by Django 3.0.7 on 2021-07-30 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multichoice', '0003_auto_20210729_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='content',
            field=models.CharField(help_text='Câu trả lời', max_length=1000, verbose_name='Nội dung'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='correct',
            field=models.BooleanField(default=False, help_text='Câu trả lời đúng', verbose_name='Tick vào câu trả lời đúng'),
        ),
        migrations.AlterField(
            model_name='mcquestion',
            name='answer_order',
            field=models.CharField(blank=True, choices=[('content', 'Nội dung'), ('random', 'Ngẫu nhiên'), ('none', 'Không chọn')], help_text='Cách thức hiển thị câu trả lời trên bài thi', max_length=30, null=True, verbose_name='Thứ tự câu trả lời'),
        ),
    ]