# Generated by Django 2.0.3 on 2018-04-08 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_ui', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=300)),
                ('price', models.CharField(max_length=50)),
                ('rating', models.CharField(max_length=50)),
                ('noOfReviews', models.CharField(max_length=50)),
                ('savings', models.CharField(max_length=50)),
                ('percentageSavings', models.CharField(max_length=50)),
                ('reviewPolarity', models.CharField(max_length=50)),
                ('countryOfOrigin', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='note',
            name='user',
        ),
        migrations.DeleteModel(
            name='Note',
        ),
    ]
