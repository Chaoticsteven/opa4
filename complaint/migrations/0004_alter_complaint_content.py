# Generated by Django 3.2.5 on 2022-06-09 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0003_alter_complaint_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='content',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]