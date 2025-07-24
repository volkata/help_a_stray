from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView, DetailView

import district
from district.models import District


# Create your views here.
def home(request):
    districts = District.objects.annotate(
        cat_count = Count('cats')
    ).order_by('cat_count')
    return render(request, 'district/home_page.html', {'districts': districts})

class CatsInDistrictListView(DetailView):
    model = District
    template_name = 'district/district_cats.html'
    context_object_name = 'district'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add all cats in this district to the context
        context['cats'] = self.object.cats.all()
        return context

    def get_template_names(self):
        if self.object.cats.exists():
            return ['district/district_cats.html']
        else:
            return ['district/district_no_cats.html']