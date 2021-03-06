# Generated by Django 3.1 on 2021-08-18 06:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import koytola.account.models
import koytola.core.db.fields
import koytola.core.utils
import koytola.core.utils.editorjs
import phonenumber_field.modelfields
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificateType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Company', 'Company'), ('Product', 'Product')], max_length=250)),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=koytola.core.utils.upload_path_handler)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('publication_date', models.DateField(blank=True, null=True)),
                ('update_date', models.DateField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('seo_title', models.CharField(blank=True, max_length=70, null=True, validators=[django.core.validators.MaxLengthValidator(70)])),
                ('seo_description', models.CharField(blank=True, max_length=300, null=True, validators=[django.core.validators.MaxLengthValidator(300)])),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True, unique=True)),
                ('website', models.URLField(blank=True, default='')),
                ('phone', koytola.account.models.PossiblePhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('logo', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=koytola.core.utils.upload_path_handler)),
                ('logo_alt', models.CharField(blank=True, max_length=128)),
                ('founded_year', models.IntegerField(blank=True, default=2021, null=True, validators=[django.core.validators.MaxValueValidator(2100), django.core.validators.MinValueValidator(1800)])),
                ('no_of_employees', models.CharField(blank=True, choices=[('1-10', '1-10'), ('11-50', '11-50'), ('51-200', '51-200'), ('201-500', '201-500'), ('501-1000', '501-1000'), ('1001-5000', '1001-5000'), ('5001-10,000', '5001-10,000'), ('10,000+', '10,000+')], default='1-10', max_length=32, null=True)),
                ('content', koytola.core.db.fields.SanitizedJSONField(blank=True, default=dict, sanitizer=koytola.core.utils.editorjs.clean_editor_js)),
                ('content_plaintext', models.TextField(blank=True, null=True)),
                ('vision', models.TextField(blank=True, null=True)),
                ('brands', models.TextField(blank=True, default='[]')),
                ('membership', models.TextField(blank=True, default='[]')),
                ('is_brand', models.BooleanField(default=False)),
                ('export_countries', django_countries.fields.CountryField(blank=True, max_length=746, multiple=True)),
                ('size', models.CharField(choices=[('none', 'No company size is chosen'), ('small_business', 'Small business'), ('medium_business', 'Medium size business'), ('large_enterprise', 'Large enterprise')], default='none', max_length=32)),
                ('type', models.CharField(choices=[('manufacturer', 'Manufacturer company type'), ('supplier', 'Supplier company type')], default='manufacturer', max_length=32)),
                ('organic_products', models.BooleanField(default=False)),
                ('private_label', models.BooleanField(default=False)),
                ('female_leadership', models.BooleanField(default=False)),
                ('branded_value', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.address')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
                'ordering': ['slug'],
                'permissions': [('manage_profiles', 'Manage profiles.')],
            },
        ),
        migrations.CreateModel(
            name='Roetter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Company', 'Company'), ('Product', 'Product')], max_length=250)),
                ('name', models.CharField(max_length=250)),
                ('category', models.TextField(blank=True, max_length=65500, null=True)),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='rosetter/')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SuccessStory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.CharField(blank=True, max_length=65550, null=True)),
                ('image', models.ImageField(blank=True, upload_to=koytola.core.utils.upload_path_handler)),
                ('location', models.CharField(blank=True, max_length=250, null=True)),
                ('company_name', models.CharField(blank=True, max_length=250, null=True)),
                ('slug', models.CharField(blank=True, max_length=250, null=True)),
                ('tags', models.TextField(blank=True, default='[]', max_length=6550)),
                ('is_active', models.BooleanField(default=True)),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(db_index=True, editable=False, null=True)),
                ('video', models.FileField(blank=True, upload_to=koytola.core.utils.upload_path_handler)),
                ('youtube_url', models.URLField(blank=True)),
                ('name', models.CharField(blank=True, max_length=128)),
                ('index', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=128)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='videos', to='profile.company')),
            ],
            options={
                'verbose_name': 'Company Video',
                'verbose_name_plural': 'Company Videos',
                'ordering': ['sort_order', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='TradeShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('year', models.IntegerField()),
                ('city', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_trade_show', to='profile.company')),
            ],
        ),
        migrations.CreateModel(
            name='SocialResponsibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(db_index=True, editable=False, null=True)),
                ('name', models.CharField(blank=True, max_length=128)),
                ('video', models.FileField(blank=True, upload_to=koytola.core.utils.upload_path_handler)),
                ('youtube_url', models.URLField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to=koytola.core.utils.upload_path_handler)),
                ('brochure', models.FileField(blank=True, upload_to=koytola.core.utils.upload_path_handler)),
                ('brochure_file_name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, max_length=65500)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='social_responsibilities', to='profile.company')),
            ],
            options={
                'verbose_name': 'Company Social Responsibility',
                'verbose_name_plural': 'Company Social Responsibilities',
                'ordering': ['sort_order', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=koytola.core.utils.upload_path_handler)),
                ('photo_alt', models.CharField(blank=True, max_length=128)),
                ('name', models.CharField(max_length=250)),
                ('position', models.CharField(default='Customer Representative', max_length=250)),
                ('linkedin_url', models.CharField(blank=True, max_length=250)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='representative', to='profile.company')),
            ],
            options={
                'verbose_name': 'Company Representative',
                'verbose_name_plural': 'Company Representatives',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='profile.industry')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(db_index=True, editable=False, null=True)),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=koytola.core.utils.upload_path_handler)),
                ('name', models.CharField(blank=True, max_length=128)),
                ('index', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=128)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='profile.company')),
            ],
            options={
                'verbose_name': 'Company Images',
                'verbose_name_plural': 'Company Images',
                'ordering': ['sort_order', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32)),
                ('email', models.EmailField(blank=True, max_length=64)),
                ('country', models.CharField(blank=True, max_length=64)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('ask_for_reference', models.BooleanField(default=False)),
                ('subject', models.CharField(blank=True, max_length=128, null=True)),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('type', models.CharField(blank=True, choices=[('info', 'Info message type'), ('quotation', 'Quotation message type'), ('other', 'Other message type')], default='info', max_length=32)),
                ('status', models.CharField(blank=True, choices=[('new', 'New message'), ('ongoing', 'Message status is ongoing'), ('done', 'Message is done'), ('spam', 'Message marked as spam')], default='new', max_length=32)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_messages', to='profile.company')),
            ],
            options={
                'verbose_name': 'Company Contact Data',
                'verbose_name_plural': 'Company Contact Data',
                'ordering': ['-submission_date'],
            },
        ),
        migrations.AddField(
            model_name='company',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_industry', to='profile.industry'),
        ),
        migrations.AddField(
            model_name='company',
            name='rosetter',
            field=models.ManyToManyField(blank=True, related_name='_company_rosetter_+', to='profile.Roetter'),
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(db_index=True, editable=False, null=True)),
                ('certificate', models.FileField(blank=True, upload_to=koytola.core.utils.upload_path_handler)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='certificates', to='profile.company')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='certificate_type', to='profile.certificatetype')),
            ],
            options={
                'verbose_name': 'Company Certificate',
                'verbose_name_plural': 'Company Certificates',
                'ordering': ['sort_order', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='Brochure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(db_index=True, editable=False, null=True)),
                ('brochure', models.FileField(blank=True, upload_to=koytola.core.utils.upload_path_handler)),
                ('name', models.CharField(blank=True, max_length=128)),
                ('index', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=128)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brochures', to='profile.company')),
            ],
            options={
                'verbose_name': 'Company Brochure',
                'verbose_name_plural': 'Company Brochures',
                'ordering': ['sort_order', 'pk'],
            },
        ),
    ]
