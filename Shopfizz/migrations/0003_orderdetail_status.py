# Generated by Django 4.1 on 2022-08-30 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shopfizz', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Deliverd', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=50),
        ),
    ]