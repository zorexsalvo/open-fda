# Generated by Django 2.2.4 on 2019-08-14 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0002_term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='amount',
            field=models.IntegerField(help_text='in cents'),
        ),
    ]