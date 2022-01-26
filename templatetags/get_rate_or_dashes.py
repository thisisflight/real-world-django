from django import template
from events.models import Review

register = template.Library()


@register.simple_tag
def get_rate_or_dashes(event, user):
    review = Review.objects.filter(event=event, user=user).first()
    return review.rate if review else '--'
