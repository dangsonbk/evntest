# Generated by Django 3.0.7 on 2021-07-30 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20210730_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.Branch', verbose_name='Công ty'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.Department', verbose_name='Phòng ban'),
        ),
        migrations.AlterField(
            model_name='question',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.Branch', verbose_name='Công ty'),
        ),
        migrations.AlterField(
            model_name='question',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.Department', verbose_name='Phòng ban'),
        ),
        migrations.AlterField(
            model_name='question',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.Grade', verbose_name='Bậc thợ'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.Grade', verbose_name='Bậc thợ'),
        ),
    ]
