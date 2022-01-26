from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import EnrollToEventForm, EventCreateUpdateForm
from .models import Event, Review, Enroll


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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-pk')


class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['enroll_form'] = EnrollToEventForm(initial={'user': self.request.user,
                                                            'event': self.object})
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
        context['title'] = f'Редактирование события {self.object.title}'
        context['enrolls'] = self.object.enrolls.all()
        context['reviews'] = self.object.reviews.all()
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


@require_POST
def create_review(request):
    data = {}
    is_user_authenticated = True if request.user.is_authenticated else False
    review_exists = False
    event_id = request.POST.get('event_id')
    rate = request.POST.get('rate')
    text = request.POST.get('text')
    if (all([event_id, rate, text])
            and Event.objects.filter(pk=event_id).first()
            and is_user_authenticated):
        event = Event.objects.get(pk=event_id)
        is_user_already_reviewed = Event.objects.filter(reviews__user=request.user).exists()
        if not is_user_already_reviewed:
            review = Review.objects.create(
                user=request.user,
                event=event,
                rate=rate,
                text=text
            )
            data['ok'] = True
            data['msg'] = ''
            data['rate'] = rate
            data['text'] = text
            data['created'] = review.created
            data['user_name'] = request.user.username
            return JsonResponse(data)
        else:
            review_exists = True
    data['ok'] = False
    if not event_id:
        data['msg'] = 'Не назначено событие для отзыва'
    elif not rate:
        data['msg'] = 'Не поставлена оценка событию'
    elif not text:
        data['msg'] = 'Нет текста отзыва'
    elif review_exists:
        data['msg'] = 'Вы уже оценили это событие ранее'
    elif not is_user_authenticated:
        data['msg'] = 'Отзывы могут оставлять только зарегистрированные пользователи'
    data['rate'] = rate
    data['text'] = text
    data['created'] = ''
    data['user_name'] = ''
    return JsonResponse(data)
