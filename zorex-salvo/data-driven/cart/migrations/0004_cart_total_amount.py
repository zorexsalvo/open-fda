# Generated by Django 2.2.4 on 2019-08-14 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20190814_0445'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_amount',
            field=models.IntegerField(default=0, help_text='in cents'),
            preserve_default=False,
        ),
    ]