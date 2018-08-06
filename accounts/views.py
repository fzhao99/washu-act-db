from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .forms import SignUpForm

# Create your views here.
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'myaccount.html'
    success_url = reverse_lazy('account_settings')

    def get_object(self):
        return self.request.user


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
