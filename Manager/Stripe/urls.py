from django.conf.urls import url, include

urlpatterns = [
    url(r'^invoices/', include('Manager.Stripe.Invoice.urls')),
]
