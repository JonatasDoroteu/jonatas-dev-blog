import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from blog.models import Category, Tag

print('Existing categories:', list(Category.objects.values_list('slug', flat=True)))
print('Existing tags:', list(Tag.objects.values_list('slug', flat=True)))

# If none exist, create sample ones
created = False
if Category.objects.count() == 0:
    Category.objects.bulk_create([
        Category(name='Backend', slug='backend'),
        Category(name='Frontend', slug='frontend'),
        Category(name='DevOps', slug='devops'),
    ])
    created = True
if Tag.objects.count() == 0:
    Tag.objects.bulk_create([
        Tag(name='Django', slug='django'),
        Tag(name='Python', slug='python'),
        Tag(name='API', slug='api'),
    ])
    created = True

if created:
    print('Sample categories and tags were created.')
else:
    print('No changes needed.')
