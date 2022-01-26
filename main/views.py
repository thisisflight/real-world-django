from django.views.generic import TemplateView

from events.models import Event, Review


class MainPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all().order_by('-pk')[:3]
        context['reviews'] = Review.objects.all().order_by('-pk')[:3]
        context['flag'] = True
        context['main'] = True
        return context
