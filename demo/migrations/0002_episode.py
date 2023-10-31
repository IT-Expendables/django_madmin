# Generated by Django 4.2.5 on 2023-10-30 17:19

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.CharField(max_length=1000, verbose_name='视频')),
                ('article', models.ForeignKey(on_delete=django.db.models.expressions.Case, to='demo.article', verbose_name='剧集')),
            ],
            options={
                'verbose_name': '单集',
                'verbose_name_plural': '单集列表',
            },
        ),
    ]
