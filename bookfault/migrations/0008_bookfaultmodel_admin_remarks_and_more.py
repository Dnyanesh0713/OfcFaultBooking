# Generated by Django 5.1.2 on 2024-11-12 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookfault', '0007_bookfaultmodel_total_downtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookfaultmodel',
            name='Admin_Remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookfaultmodel',
            name='Transnet_ID',
            field=models.CharField(default='', max_length=10),
        ),
    ]
