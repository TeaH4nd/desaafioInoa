# Generated by Django 3.1.5 on 2021-01-07 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotaAtivos', '0006_auto_20210106_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
            ],
        ),
    ]
