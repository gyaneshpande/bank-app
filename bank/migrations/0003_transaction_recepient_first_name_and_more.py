# Generated by Django 5.0.4 on 2024-05-05 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0002_alter_account_cust_id_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='recepient_first_name',
            field=models.CharField(default='test', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='recepient_last_name',
            field=models.CharField(default='test_last_name', max_length=30),
            preserve_default=False,
        ),
    ]