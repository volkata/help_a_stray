from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView, DetailView

import district
from district.models import District

User = get_user_model()

# Create your views here.
def home(request):
    districts = District.objects.annotate(
        cat_count = Count('cats')
    ).order_by('name')
    return render(request, 'district/home_page.html', {'districts': districts})

class CatsInDistrictListView(LoginRequiredMixin, DetailView):
    model = District
    template_name = 'district/district_cats.html'
    context_object_name = 'district'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        approved_cats = self.object.cats.filter(approved=True)
        context['approved_cats'] = approved_cats
        non_approved_cats = None
        if user.is_district_admin():
            if user.main_district.id == self.object.id:
                non_approved_cats = self.object.cats.filter(approved=False)
        context['non_approved_cats'] = non_approved_cats
        return context

    def get_template_names(self):
        if self.object.cats.exists():
            return ['district/district_cats.html']
        else:
            return ['district/district_no_cats.html']