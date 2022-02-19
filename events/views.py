from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import (EnrollToEventForm, EventCreateUpdateForm,
                    EventFilterForm, EventAddToFavoriteForm, ReviewForm)
from .models import Event, Review, Enroll, Favorite


class LoginRequiredMixin:
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Недостаточно прав')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Недостаточно прав')
        return super().post(request, *args, **kwargs)


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = EventFilterForm(self.request.GET)
        is_filter_used = bool(self.request.GET)
        if is_filter_used:
            context['query'] = '&'.join(['='.join(item) for item in self.request.GET.items()])
        context['is_filter_used'] = is_filter_used
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('features', 'enrolls')
        form = EventFilterForm(self.request.GET)
        if form.is_valid():
            filter_category = form.cleaned_data.get('category')
            filter_features = form.cleaned_data.get('features')
            filter_date_start = form.cleaned_data.get('date_start')
            filter_date_end = form.cleaned_data.get('date_end')
            filter_is_private = form.cleaned_data.get('is_private')
            filter_is_available = form.cleaned_data.get('is_available')
            if filter_category:
                queryset = queryset.filter(category=filter_category)
            if filter_features:
                for feature in filter_features:
                    queryset = queryset.filter(features__in=[feature])
            if filter_date_start:
                queryset = queryset.filter(date_start__gte=filter_date_start)
            if filter_date_end:
                queryset = queryset.filter(date_start__lte=filter_date_end)
            if filter_is_private:
                queryset = queryset.filter(is_private=True)
            if filter_is_available:
                queryset = [event for event in queryset if event.places_left]
            return sorted(queryset, key=lambda event: event.pk, reverse=True)
        return queryset.order_by('-pk')


class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user, event = self.request.user, self.object
        form_data = {'user': user, 'event': event}
        context['reviews'] = event.reviews.select_related('user', 'event').all()
        context['enroll_form'] = EnrollToEventForm(initial=form_data)
        context['favorite_form'] = EventAddToFavoriteForm(initial=form_data)
        if user.is_authenticated:
            context['in_favorites'] = bool(Favorite.objects.filter(user=user, event=event))
        context['review_form'] = ReviewForm(initial=form_data)
        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    template_name = 'events/event_update.html'
    form_class = EventCreateUpdateForm
    success_url = reverse_lazy('events:event_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание события'
        return context


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = 'events/event_update.html'
    form_class = EventCreateUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrolls = self.object.enrolls.select_related('user', 'event').all()
        reviews = self.object.reviews.select_related('user', 'event').all()
        reviews_rates = {review.user_id: review.rate for review in reviews}
        context['title'] = f'Редактирование события {self.object.title}'
        context['enrolls'] = enrolls
        context['reviews'] = reviews
        context['reviews_rates'] = reviews_rates
        return context


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_update.html'
    success_url = reverse_lazy('events:event_list')
    context_object_name = 'delete_form'

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f'Событие {self.object} удалено')
        return result


class EventCreateReview(CreateView):
    model = Review
    form_class = ReviewForm

    def get_success_url(self):
        return self.object.event.get_absolute_url()

    def form_valid(self, form):
        messages.success(self.request, f'Вы оставили отзыв на событие {form.cleaned_data["event"]}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        event = form.cleaned_data.get('event', None)
        if not event:
            event = get_object_or_404(Event, pk=form.data.get('event'))
        redirect_url = event.get_absolute_url() if event else reverse_lazy('events:event_list')
        return HttpResponseRedirect(redirect_url)


class EnrollToEventView(LoginRequiredMixin, CreateView):
    model = Enroll
    form_class = EnrollToEventForm

    def get_success_url(self):
        return self.object.event.get_absolute_url()

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        event = form.cleaned_data.get('event', None)
        if not event:
            event = get_object_or_404(Event, pk=form.data.get('event'))
        redirect_url = event.get_absolute_url() if event else reverse_lazy('events:event_list')
        return HttpResponseRedirect(redirect_url)

    def form_valid(self, form):
        messages.success(self.request, f'Вы успешно записаны на событие {form.cleaned_data["event"]}')
        return super().form_valid(form)


class EventAddToFavoriteView(LoginRequiredMixin, CreateView):
    model = Favorite
    form_class = EventAddToFavoriteForm

    def get_success_url(self):
        return self.object.event.get_absolute_url()

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        event = form.cleaned_data.get('event', None)
        if not event:
            event = get_object_or_404(Event, pk=form.data.get('event'))
        redirect_url = event.get_absolute_url() if event else reverse_lazy('events:event_list')
        return HttpResponseRedirect(redirect_url)

    def form_valid(self, form):
        messages.success(self.request, f'Событие {form.cleaned_data["event"]} добавлено в избранное')
        return super().form_valid(form)
