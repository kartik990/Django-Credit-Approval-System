# Generated by Django 5.0.2 on 2024-02-17 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit_approval', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='loan_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
