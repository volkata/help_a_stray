from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from rest_framework import viewsets

from actions.forms import ActionEditForm
from actions.models import Action
from actions.serializers import ActionSerializer
from cat.models import Cat


# Create your views here.
class ActionsListView(ListView):
    model = Action
    template_name = 'actions/actions_list.html'
    context_object_name = 'actions'
    priority_order = ['High', 'Medium', 'Low']

    def get_queryset(self):
        # Sort by priority: High, Medium, Low
        order_map = {p: i for i, p in enumerate(self.priority_order)}
        actions = list(Action.objects.all())
        sorted_actions = sorted(
            actions,
            key=lambda action:  order_map.get(action.priority, len(self.priority_order))
        )
        return sorted_actions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        context['high_priority'] = [a for a in queryset if a.priority == 'High']
        context['medium_priority'] = [a for a in queryset if a.priority == 'Medium']
        context['low_priority'] = [a for a in queryset if a.priority == 'Low']
        context['newly_added'] = [a for a in queryset if a.priority not in self.priority_order]

        # newly added Health notes cats visible only to vets
        if self.request.user.is_vet():
            health_cats = {
                a.cat
                for a in context['newly_added']
                if a.action_type == 'Health issue' and a.cat.health_notes
            }
            context['health_cats'] = health_cats

        return context

def vet_required(user):
    return user.is_vet()


@user_passes_test(vet_required)
def edit_action(request, cat_id):
    action = get_object_or_404(Action, cat_id=cat_id, action_type='Health issue')
    if request.method == 'POST':
        form = ActionEditForm(request.POST, instance=action)
        if form.is_valid():
            form.save()
            return redirect('cat_detail', pk=cat_id)
    else:
        form = ActionEditForm(instance=action)
    return render(request, 'actions/edit_action.html', {'form': form, 'action': action})

@login_required
def contribute_treatment(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)


    if request.method == "POST":
        try:
            contribution = float(request.POST.get("amount", 0))
            if contribution <= 0:
                messages.error(request, "Contribution must be greater than zero.")
                return redirect('cat_detail', pk=cat.id)

            total_due = sum(a.treatment_cost for a in cat.actions.all() if a.treatment_cost > 0)

            if contribution < total_due:
                messages.error(request, f"Contribution is less than total treatment cost (${total_due:.2f}).")
                return redirect('cat_detail', pk=cat.id)

            cat.actions.filter(treatment_cost__gt=0).delete() #keeps all undiagnosed by vet health notes

            profile = request.user.profile
            profile.karma_points += int(contribution)
            profile.save()
            messages.success(request, f"Thank you for contributing ${contribution:.2f}!")

        except ValueError:
            messages.error(request, "Invalid contribution amount.")

    return redirect('cat_detail', pk=cat.id)

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer