# Generated by Django 5.0.4 on 2024-04-19 17:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Escola', '0002_remove_atividade_id_professor_atividade_id_turma'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='id_turma',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App_Escola.turma'),
        ),
    ]
