import django.dispatch

invitation_sent = django.dispatch.Signal(providing_args=["user"])
