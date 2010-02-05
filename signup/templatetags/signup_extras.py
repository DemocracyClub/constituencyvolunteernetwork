from django import template
from datetime import datetime, timedelta
from signup.models import CustomUser
from shorten.models import Shortened

register = template.Library()
 
MOMENT = 120    # duration in seconds within which the time difference 
                # will be rendered as 'a moment ago'
 
@register.filter
def naturalTimeDifference(value):
    """Finds the difference between the datetime value given and now()
    and returns appropriate humanize form
    """

    if isinstance(value, timedelta):
        delta = value
    elif isinstance(value, datetime):
        delta = datetime.now() - value        
    else:
        delta = None

    if delta:
        if delta.days > 6:
            return value.strftime("%b %d") # May 15
        if delta.days > 1:
            return value.strftime("%A") # Wednesday
        elif delta.days == 1:
            return 'yesterday'
        elif delta.seconds >= 7200:
            return str(delta.seconds / 3600 ) + ' hours ago'
        elif delta.seconds >= 3600:
            return '1 hour ago' 
        elif delta.seconds > MOMENT:
            return str(delta.seconds/60) + ' minutes ago' 
        else:
            return 'a moment ago' 
    else:
        return str(value)

@register.filter
def shorten(url):
    #api_url = "http://api.bit.ly/shorten?version=2.0.1&longUrl=%s&login=democlub&apiKey=R_d97512b89021d2c7503f87630821f5dd " % url
    #resp = urllib.urlopen(api_url)
    #return resp.read()
    return Shortened.objects.make(url, "constituency link")

@register.filter
def user_get_name(user):
    try:
        return CustomUser.objects.get(id=user.id).display_name
    except CustomUser.DoesNotExist:
        return "Admin"
       
