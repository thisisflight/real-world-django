from django import template

register = template.Library()


@register.simple_tag
def get_rate_or_0(reviews_rates, user_id):
    rate = reviews_rates.get(user_id)
    if rate:
        return rate
    return 0
