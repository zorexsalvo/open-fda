# Generated by Django 2.2.4 on 2019-08-14 04:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='identifier',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255, unique=True),
        ),
    ]
