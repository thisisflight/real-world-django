from threading import Thread

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from mail.models import Subscriber, Letter


@require_POST
def create_letters_view(request):
    emails = request.POST.getlist('email', None)
    subject = request.POST.get('subject', '')
    text = request.POST.get('text', '')
    if emails and subject and text:
        Letter.create_letters(emails, subject, text)

    return JsonResponse({'subscribers': Subscriber.get_objects_list()})


@require_POST
def send_letters_view(request):
    unsent_letters = Letter.objects.select_related('to').filter(is_sent=False)
    if unsent_letters:

        for index in range(0, len(unsent_letters), 10):
            current_partial = unsent_letters[index:index + 10]
            threads_list = []

            for letter in current_partial:
                sending_data = {
                    "subject": letter.subject,
                    "message": letter.text,
                    "from_email": settings.EMAIL_HOST_USER,
                    "recipient_list": [letter.to.email],
                    "fail_silently": False
                }
                thread = Thread(target=send_mail, kwargs=sending_data,)
                thread.start()
                threads_list.append(thread)
                letter.is_sent = True
                letter.save()

            while threads_list:
                for thread in threads_list:
                    if not thread.is_alive():
                        threads_list.remove(thread)

    return HttpResponseRedirect(reverse('mail:subscriber_list'))


def get_subscribers(request):
    subscribers = Subscriber.get_objects_list()
    all_emails_sent = False if bool(Letter.objects.filter(is_sent=False)) else True
    data = {
        "subscribers": subscribers,
        "all_emails_sent": all_emails_sent
    }

    return JsonResponse(data=data)
