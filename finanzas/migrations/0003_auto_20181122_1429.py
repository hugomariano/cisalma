# Generated by Django 2.0.4 on 2018-11-22 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0002_auto_20181120_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagocliente',
            name='recibo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pagoproveedor',
            name='recibo',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]