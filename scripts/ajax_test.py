import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django
django.setup()
from django.test import Client
c=Client()
from django.contrib.auth import get_user_model
User=get_user_model()
if not User.objects.filter(username='apitest').exists():
    User.objects.create_user('apitest','apitest@example.com','password')
logged_in = c.login(username='apitest',password='password')
print('logged_in', logged_in)
resp = c.post('/blog/ajax/create-category/', {'name':'Quick Cat'})
print('create-category', resp.status_code, resp.json() if resp.status_code==200 else resp.content)
resp = c.post('/blog/ajax/create-tag/', {'name':'Quick Tag'})
print('create-tag', resp.status_code, resp.json() if resp.status_code==200 else resp.content)
