from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .models import Event, Review


def get_event_list(request):
    event_list = Event.objects.all()
    context = {'events': event_list}
    return render(request, 'events/event_list.html', context)


def get_event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    reviews = event.reviews.all()
    context = {
        'event': event,
        'reviews': reviews
    }
    return render(request, 'events/event_detail.html', context)


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
        data['msg'] = 'Отзывы могут оставлять только зарегистированные пользователи'
    data['rate'] = rate
    data['text'] = text
    data['created'] = ''
    data['user_name'] = ''
    return JsonResponse(data)
