from django import template

register = template.Library()


@register.simple_tag
def get_rate_or_0(event, enroll):
    review = enroll.user.reviews.filter(event=event).first()
    return review.rate if review else 0
