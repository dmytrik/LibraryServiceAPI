# Generated by Django 5.1.4 on 2025-01-02 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63, unique=True)),
                ('author', models.CharField(max_length=63)),
                ('cover', models.CharField(choices=[('HARD', 'Hard'), ('SOFT', 'Soft')], default='SOFT', max_length=4)),
                ('inventory', models.PositiveIntegerField()),
                ('daily_fee', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]