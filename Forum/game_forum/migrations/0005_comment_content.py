# Generated by Django 4.1.7 on 2023-03-08 21:52

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_forum', '0004_post_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]