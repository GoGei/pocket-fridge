from django_hosts import reverse
from django.contrib.auth.decorators import login_required

my_login_required = login_required(login_url=reverse('login', host='public'))
