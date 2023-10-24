from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django_hosts import reverse

from My import utils, decorators
from core.Notifications.models import NotificationMessage
from core.Fridge.models import Fridge


@decorators.my_login_required
def home_index(request):
    fridge_qs = utils.get_fridge_qs(request.user)
    # return render(request, 'My/home_index.html', {'fridge_qs': fridge_qs})

    slug = Fridge.DEFAULT_SLUG_TO_DISPLAY
    default_fridge = fridge_qs.filter(fridge_type__slug=slug).first()
    if not default_fridge:
        default_fridge = fridge_qs.order_by('name').first()

    return redirect(reverse('fridge-view', kwargs={'fridge_id': default_fridge.id}, host='my'))


@decorators.my_login_required
def notifications(request):
    notifications_qs = request.user.get_notifications()
    return render(request, 'My/notifications.html', {'notifications': notifications_qs})


@decorators.my_login_required
def notifications_clear_all(request):
    notifications_qs = request.user.get_notifications()
    notifications_qs.delete()
    return redirect(reverse('notifications', host='my'))


@decorators.my_login_required
def notifications_remove(request, notification_id):
    NotificationMessage.objects.filter(id=notification_id).delete()
    return redirect(reverse('notifications', host='my'))


def logout_view(request):
    logout(request)
    return redirect(reverse('login', host='public'))
