# Generated by Django 5.1.2 on 2024-10-27 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookfault', '0003_bookfaultmodel_is_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookfaultmodel',
            name='OFC_Type',
            field=models.CharField(default='', max_length=100),
        ),
    ]
