# Generated by Django 3.2.5 on 2021-07-06 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='Avatar/default.png', upload_to='Avatar', verbose_name='avatar'),
        ),
    ]