# Generated by Django 2.2 on 2019-07-24 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userm', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='followcontact',
            options={'ordering': ('-created',), 'verbose_name': 'Contact', 'verbose_name_plural': 'Contacts'},
        ),
        migrations.AddField(
            model_name='followcontact',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userextendedr',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='userm.FollowContact', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followcontact',
            name='user_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_from_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followcontact',
            name='user_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_to_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
