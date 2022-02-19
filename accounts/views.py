from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import (LoginView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from events.models import Event, Review
from .forms import (CustomUserCreationForm, CustomAuthenticationForm,
                    ChangeProfileImageForm, CustomPasswordResetForm,
                    CustomSetPasswordForm)
from .models import Profile


class CustomSignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/registration/signup.html'
    success_url = reverse_lazy('main:index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        result = super().form_valid(form)
        username = form.cleaned_data['username']
        login(self.request, user=User.objects.get(username=username))
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = True
        return context


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/registration/signin.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = True
        return context


class UserProfilePageView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ChangeProfileImageForm
    template_name = 'profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        events = Event.objects.filter(enrolls__user=user)
        reviews = Review.objects.select_related('event').filter(user=user)
        reviews_rates = {review.event_id: review.rate for review in reviews}
        context['events'] = events
        context['reviews'] = reviews
        context['reviews_rates'] = reviews_rates
        return context


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/registration/password_reset_form.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/registration/password_reset_email.txt'
    subject_template_name = 'accounts/registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    from_email = settings.EMAIL_HOST_USER
    html_email_template_name = 'accounts/registration/password_reset_email.html'

    def form_valid(self, form):
        self.request.session['reset_email'] = form.cleaned_data['email']
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_email'] = self.request.session.get('reset_email', '')
        return context


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/registration/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/registration/password_reset_complete.html'
