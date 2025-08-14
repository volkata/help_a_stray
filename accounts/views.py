from urllib.request import Request

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accounts.forms import AppUserCreationForm, ProfileEditForm, ProfileDeleteForm, UserEditForm
from accounts.models import Profile

# Create your views here.
UserModel = get_user_model()

class RegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home')
    #uses signal to create profile
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats_interacted'] = self.object.cats_interacted.all()
        context['has_interacted'] = self.object.cats_interacted.exists()
        context['default_district'] = self.object.user.main_district
        return context

@login_required
def profile_edit(request, pk): #2 forms in 1 view for User and Profile
    profile = get_object_or_404(Profile, pk=pk)
    user = profile.user
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect(reverse_lazy('profile-details', kwargs={'pk': profile.pk}))
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form, 'profile_form': profile_form, 'profile': profile})

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'accounts/profile-delete.html'
    success_url = reverse_lazy('home')