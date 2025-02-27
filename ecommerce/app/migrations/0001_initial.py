# Generated by Django 5.1.5 on 2025-02-04 10:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Main_cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('phn', models.IntegerField()),
                ('pin', models.IntegerField()),
                ('loc', models.TextField()),
                ('adrs', models.TextField()),
                ('city', models.TextField()),
                ('state', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_name', models.TextField()),
                ('m_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.main_cat')),
            ],
        ),
        migrations.CreateModel(
            name='Plants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_id', models.TextField()),
                ('name', models.TextField()),
                ('p_catg', models.TextField()),
                ('p_dis', models.TextField()),
                ('price', models.IntegerField()),
                ('offer_price', models.IntegerField()),
                ('img', models.FileField(upload_to='')),
                ('img2', models.FileField(upload_to='')),
                ('catg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Plants', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.plants')),
            ],
        ),
    ]
