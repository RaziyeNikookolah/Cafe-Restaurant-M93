

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=14)),
                ('birthday', models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 7, 4)), django.core.validators.MinValueValidator(limit_value=datetime.date(1923, 7, 4))])),
                ('address', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'user_sessions',
                'ordering': ('-updated_at', '-created_at'),
            },
        ),
    ]
