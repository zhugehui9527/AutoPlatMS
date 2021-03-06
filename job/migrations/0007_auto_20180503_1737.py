# Generated by Django 2.0.5 on 2018-05-03 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_auto_20180502_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmanager',
            name='eamil_config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.EmailConfig', verbose_name='发件人'),
        ),
        migrations.AlterField(
            model_name='emailmanager',
            name='email_periodictask',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='periodictask_email', to='djcelery.PeriodicTask', verbose_name='定时任务'),
        ),
    ]
