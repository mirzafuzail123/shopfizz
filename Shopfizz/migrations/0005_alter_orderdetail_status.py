# Generated by Django 4.1 on 2022-08-30 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shopfizz', '0004_alter_orderdetail_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='status',
            field=models.CharField(choices=[('Order Confirmed', 'Order Confirmed'), ('Picked by courier', 'Picked by courier'), ('Ready to pickup', 'Ready to pickup')], max_length=50, null=True),
        ),
    ]
