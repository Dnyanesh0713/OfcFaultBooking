# Generated by Django 5.1.2 on 2024-11-12 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookfault', '0008_bookfaultmodel_admin_remarks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookfaultmodel',
            name='Admin_Remarks',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='bookfaultmodel',
            name='Transnet_ID',
            field=models.CharField(default='', max_length=10, null=True),
        ),
    ]
