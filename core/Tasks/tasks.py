from celery_run import app
from core.Fridge.models import FridgeProduct
from core.Notifications.models import Notification


@app.task(ignore_result=True)
def push_expired_products():
    def get_product_context(product: FridgeProduct) -> dict:
        return {
            'product_id': str(product.id),
            'product_label': product.name,
            'first_name': product.user.first_name,
            'last_name': product.user.last_name,
            'date_str': product.shelf_life_date.strftime('%d.%m.%Y'),

            'fridge_id': str(product.fridge_id),
            'amount': str(product.amount),
            'units': str(product.units),
            'notes': product.notes,
        }

    def get_with_filter(priority):
        qs = FridgeProduct.objects.active().annotate_expire_priority()
        return qs.filter(expire_priority=priority).exclude(notified_as=priority)

    expired = get_with_filter(priority=0)
    expire_today = get_with_filter(priority=1)
    expire_tomorrow = get_with_filter(priority=2)
    expire_in_3_days = get_with_filter(priority=3)

    product_will_expire = Notification.get_by_slug('product-will-expire')
    product_expired = Notification.get_by_slug('product-expired')

    for product in expired:
        product_expired.send_with_push(recipient=product.user, context=get_product_context(product))
    for product in expire_today:
        product_will_expire.send_with_push(recipient=product.user, context=get_product_context(product))
    for product in expire_tomorrow:
        product_will_expire.send_with_push(recipient=product.user, context=get_product_context(product))
    for product in expire_in_3_days:
        product_will_expire.send_with_push(recipient=product.user, context=get_product_context(product))

    expired.update(notified_as=0)
    expire_today.update(notified_as=1)
    expire_tomorrow.update(notified_as=2)
    expire_in_3_days.update(notified_as=3)
