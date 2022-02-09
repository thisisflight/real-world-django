from django import template

register = template.Library()


@register.simple_tag
def get_rate_or_dashes(reviews_rates, event_id):
    rate = reviews_rates.get(event_id)
    if rate:
        return rate
    return '--'
