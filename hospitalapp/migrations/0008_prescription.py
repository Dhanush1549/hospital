# Generated by Django 4.2.8 on 2024-01-14 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospitalapp', '0007_remove_pharmacy_recent_prescriptions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitalapp.appointment')),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitalapp.consultation')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitalapp.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitalapp.patient')),
            ],
        ),
    ]
