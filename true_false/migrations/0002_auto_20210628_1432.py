# Generated by Django 3.1 on 2021-06-28 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('true_false', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tf_question',
            options={'ordering': ['category'], 'verbose_name': 'Câu hỏi True/False', 'verbose_name_plural': 'Câu hỏi True/False'},
        ),
    ]