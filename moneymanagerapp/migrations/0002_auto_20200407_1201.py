# Generated by Django 3.0.4 on 2020-04-07 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneymanagerapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='date',
            options={},
        ),
        migrations.AddField(
            model_name='date',
            name='amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
