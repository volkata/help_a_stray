from django.shortcuts import render, redirect
from rest_framework import viewsets

from cat.models import Cat
from cat.serializers import CatSerializer


# Create your views here.
def cat_detail(request, pk):
    cat = Cat.objects.get(pk=pk)
    if not cat.approved:
        if not (request.user.is_superuser or request.user.is_district_admin() and request.user.main_district == cat.district):
            return redirect('cats_in_district', pk=cat.district.pk)
    if request.method == 'POST':
        if 'approve' in request.POST:
            if request.user.is_district_admin() and request.user.main_district == cat.district:
                cat.approved = True
                cat.save()
        elif 'delete' in request.POST:
            if request.user.is_superuser or (
                    request.user.is_district_admin() and request.user.main_district == cat.district):
                cat.delete()
                return redirect('home')

    return render(request, 'cat/cat_detail.html', {'cat': cat})

class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer