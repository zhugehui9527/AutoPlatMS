# Generated by Django 2.0.5 on 2018-05-03 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0008_auto_20180503_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmanager',
            name='eamil_config',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='config.EmailConfig', verbose_name='发件人'),
        ),
        migrations.AlterField(
            model_name='emailmanager',
            name='email_periodictask',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='periodictask_email', to='djcelery.PeriodicTask', verbose_name='定时任务'),
        ),
    ]
