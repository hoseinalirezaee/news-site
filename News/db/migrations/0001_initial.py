# Generated by Django 3.0.2 on 2020-07-03 14:31

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
import jsonfield.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'},
                                              help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                              max_length=150, unique=True,
                                              validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                                              verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False,
                                                 help_text='Designates whether the user can log into this admin site.',
                                                 verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True,
                                                  help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                                                  verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True, verbose_name='agency')),
                ('code', models.CharField(max_length=25, unique=True, verbose_name='code')),
                ('image', models.URLField(blank=True, max_length=1024, null=True, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='category')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteAgency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, unique=True, verbose_name='title')),
                ('summary', models.CharField(blank=True, max_length=2000, null=True, verbose_name='summary')),
                ('main_image', models.URLField(blank=True, max_length=1024, null=True, verbose_name='main image')),
                ('date_posted', models.DateTimeField(verbose_name='date posted')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('origin_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='origin id')),
                ('origin_url', models.URLField(max_length=1024, verbose_name='origin url')),
                ('paragraphs', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='tag')),
            ],
        ),
        migrations.CreateModel(
            name='UserFavoriteCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TopPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(verbose_name='date posted')),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='top_posts',
                                              related_query_name='top_posts', to='db.Post')),
            ],
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['title'], name='db_tag_title_637273_idx'),
        ),
        migrations.AddField(
            model_name='posttag',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db.Post'),
        ),
        migrations.AddField(
            model_name='posttag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db.Tag'),
        ),
        migrations.AddField(
            model_name='post',
            name='agency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts',
                                    related_query_name='posts', to='db.Agency'),
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts',
                                    related_query_name='posts', to='db.Category'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='posts', related_query_name='posts', through='db.PostTag',
                                         to='db.Tag'),
        ),
        migrations.AddField(
            model_name='favoriteagency',
            name='agency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db.Agency'),
        ),
        migrations.AddField(
            model_name='favoriteagency',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='sub_categories', related_query_name='sub_categories',
                                    to='db.Category'),
        ),
        migrations.AddIndex(
            model_name='agency',
            index=models.Index(fields=['code'], name='db_agency_code_148927_idx'),
        ),
        migrations.AddField(
            model_name='user',
            name='bookmark',
            field=models.ManyToManyField(related_name='users_who_bookmark', through='db.UserBookmark', to='db.Post'),
        ),
        migrations.AddField(
            model_name='user',
            name='favorite_agencies',
            field=models.ManyToManyField(related_name='users_who_favor', through='db.FavoriteAgency', to='db.Agency'),
        ),
        migrations.AddField(
            model_name='user',
            name='favorite_categories',
            field=models.ManyToManyField(related_name='users_who_favor', through='db.UserFavoriteCategory',
                                         to='db.Category'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True,
                                         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                         related_name='user_set', related_query_name='user', to='auth.Group',
                                         verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                         related_name='user_set', related_query_name='user', to='auth.Permission',
                                         verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='posttag',
            unique_together={('post', 'tag')},
        ),
    ]
