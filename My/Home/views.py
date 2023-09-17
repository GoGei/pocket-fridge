from django.shortcuts import render


def home_index(request):
    return render(request, 'My/home_index.html')
