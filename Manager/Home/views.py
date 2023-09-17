from django.shortcuts import render
from core.Utils.Access.decorators import manager_required


@manager_required
def manager_index(request):
    return render(request, 'Manager/manager_index.html')
