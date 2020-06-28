import pytz
from django.template import library
from jdatetime import datetime

register = library.Library()


@register.filter
def convert_date(value):
    date_time = datetime.fromgregorian(
        year=value.year,
        month=value.month,
        day=value.day,
        hour=value.hour,
        minute=value.minute,
        second=value.second,
        tzinfo=value.tzinfo
    )
    date_time = date_time.astimezone(tz=pytz.timezone('Asia/Tehran'))
    date_time = date_time.aslocale('fa_IR')

    return date_time.strftime('%d %B %Y - %H:%M')
