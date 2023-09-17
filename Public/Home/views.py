from django.shortcuts import render


def home_index(request):
    return render(request, 'Public/home_index.html')
