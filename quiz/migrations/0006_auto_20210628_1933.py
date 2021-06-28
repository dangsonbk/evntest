# Generated by Django 3.0.7 on 2021-06-28 12:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0005_auto_20210628_1821'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(blank=True, max_length=512, null=True, verbose_name='Phân loại')),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Phân loại', 'verbose_name_plural': 'Phân loại'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Thí sinh', 'verbose_name_plural': 'Thí sinh'},
        ),
        migrations.AlterModelOptions(
            name='progress',
            options={'verbose_name': 'Bài làm của thí sinh', 'verbose_name_plural': 'Bài làm của thí sinh'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'Phân loại nhỏ', 'verbose_name_plural': 'Phân loại nhỏ'},
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(blank=True, max_length=250, null=True, unique=True, verbose_name='Phân loại'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='score',
            field=models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Điểm'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Thí sinh'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='answers_at_end',
            field=models.BooleanField(default=False, help_text='Hiển thị kết quả sau khi nộp bài', verbose_name='Xem kết quả'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Category', verbose_name='Phân loại'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.TextField(blank=True, help_text='Thông tin bài thi', verbose_name='Chi tiết'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='exam_paper',
            field=models.BooleanField(default=False, help_text='Hiển thị toàn bộ câu hỏi một lần', verbose_name='Hiển thị toàn bộ câu hỏi'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='fail_text',
            field=models.TextField(blank=True, help_text='Thông báo thi trượt', verbose_name='Thông báo thi trượt'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='max_questions',
            field=models.PositiveIntegerField(blank=True, help_text='Số lượng câu hỏi tối đa.', null=True, verbose_name='Số câu hỏi'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='pass_mark',
            field=models.SmallIntegerField(blank=True, default=0, help_text='Điểm tối thiểu để đạt', validators=[django.core.validators.MaxValueValidator(100)], verbose_name='Điểm tối thiểu'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='single_attempt',
            field=models.BooleanField(default=False, help_text='Chỉ cho phép thi một lần hoặc nhiều lần', verbose_name='Thi một lần'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='success_text',
            field=models.TextField(blank=True, help_text='Thông báo thi đạt', verbose_name='Thông báo thi đạt'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='url',
            field=models.SlugField(help_text='Đường dẫn tới bài thi', max_length=60, verbose_name='Đường dẫn'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Category', verbose_name='Phân loại chính'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='sub_category',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Phân loại nhỏ'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Department', verbose_name='Phòng ban'),
        ),
    ]