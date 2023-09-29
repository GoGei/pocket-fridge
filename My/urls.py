from django.conf.urls import url, include

urlpatterns = [
    url(r'', include('urls')),
    url(r'^', include('My.Home.urls')),
    url(r'^fridge/', include('My.Fridge.urls')),
    url(r'^shopping-list/', include('My.ShoppingList.urls')),
]
