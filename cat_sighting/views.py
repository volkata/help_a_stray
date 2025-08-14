from rest_framework import viewsets

from accounts.models import Profile

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from cat.models import Cat, HealthNotes

from cat_sighting.forms import CatSightingPartOneForm, CatSightingNewForm, CatSightingExistingForm
from cat_sighting.models import CatSighting
from cat_sighting.serializers import CatSightingSerializer


# Create your views here.
@login_required
def create_sighting_part1(request):
    if request.method == 'POST':
        form = CatSightingPartOneForm(request.POST, user=request.user)
        if form.is_valid():
            request.session['part1_data'] = {
                'district_id':form.cleaned_data['district'].id,
                'color_ids':[c.id for c in form.cleaned_data['color']],
                'gender':form.cleaned_data['gender'],
            }
            request.session['cat_sighting_part1_done'] = True
            district_id = request.session['part1_data']['district_id']
            color_ids = request.session['part1_data']['color_ids']
            gender = request.session['part1_data']['gender']
            cats = Cat.objects.filter(district_id=district_id, color__in=color_ids)
            if gender != 'Unknown':
                cats = cats.filter(gender=gender)
            return render(request, 'cat_sighting/cat_filter.html',
                          {'cats':cats,
                           'district':district_id,
                           'color':color_ids,
                           'gender':gender,
                           })

        else:
            return render(request, 'cat_sighting/step1.html', {'form': form})
    else:
        form = CatSightingPartOneForm(user=request.user)
        return render(request, 'cat_sighting/step1.html', {'form': form})

@login_required
def create_sighting_existing_cat(request, pk):
    cat = get_object_or_404(Cat, id=pk)
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = CatSightingExistingForm(request.POST, instance=cat)
        if form.is_valid():
            cat = form.save(commit=False)
            gave_food = form.cleaned_data['gave_food']
            gave_water = form.cleaned_data['gave_water']
            health_notes = form.cleaned_data['health_notes']
            if gave_food:
                cat.last_fed = timezone.now()
                profile.karma_points += 15
            if gave_water:
                cat.last_water = timezone.now()
                profile.karma_points += 15
            if health_notes:
                HealthNotes.objects.create(cat=cat, condition=health_notes)
            cat.last_seen = timezone.now()
            cat.save()
            profile.cats_interacted.add(cat)
            profile.save()
            return redirect('home')
    else:
        form = CatSightingExistingForm(instance=cat)

    return render(request, 'cat_sighting/update_cat.html', {'form': form})


@login_required
def create_sighting_new_cat(request):
    part1_data = request.session.get('part1_data')
    if not part1_data:
        return redirect('/cat_sighting/step1.html')
    if request.method == 'POST':
        form = CatSightingNewForm(request.POST, request.FILES)
        form.instance.district_id = part1_data['district_id']
        form.instance.color_ids = part1_data['color_ids']
        form.instance.gender = part1_data['gender']
        if form.is_valid():
            cat = form.save()
            color_ids = part1_data.get('color_ids')
            cat.color.set(color_ids)
            gave_food = form.cleaned_data['gave_food']
            gave_water = form.cleaned_data['gave_water']
            health_notes = form.cleaned_data['health_notes']
            profile = Profile.objects.get(user=request.user)
            CatSighting.objects.create(
                user = request.user,
                cat = cat,
                district_id = part1_data['district_id'],
                gave_food = gave_food,
                gave_water = gave_water,
                time_met = timezone.now()
            )
            if gave_food:
                cat.last_fed = timezone.now()
                profile.karma_points += 15
            if gave_water:
                cat.last_water = timezone.now()
                profile.karma_points += 15
            if health_notes:
                HealthNotes.objects.create(cat=cat, condition=health_notes)
            cat.last_seen = timezone.now()
            cat.save()
            profile.cats_interacted.add(cat)
            profile.save()
            request.session.pop('part1_data', None)
            return redirect('home')
    else:
        form = CatSightingNewForm()
    return render(request, 'cat_sighting/new_cat.html', {'form': form})

class CatSightingViewSet(viewsets.ModelViewSet):
    queryset = CatSighting.objects.all()
    serializer_class = CatSightingSerializer