from django.conf.urls import url, include

urlpatterns = [
    url(r'^invoices/', include('Manager.Stripe.Invoice.urls')),
    url(r'^payments/', include('Manager.Stripe.Payment.urls')),
    url(r'^products/', include('Manager.Stripe.Product.urls')),
]
