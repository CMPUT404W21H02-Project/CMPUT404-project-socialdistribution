# Generated by Django 3.1.6 on 2021-03-01 06:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CitrusAuthor',
            fields=[
                ('type', models.CharField(default='Author', max_length=100)),
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('host', models.CharField(default='http://localhost:8000/', max_length=200)),
                ('displayName', models.CharField(default='<django.db.models.fields.related.OneToOneField>', max_length=300)),
                ('github', models.CharField(default='', max_length=300, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
