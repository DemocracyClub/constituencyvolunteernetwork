import django.dispatch

ynmp_action_done = django.dispatch.Signal(providing_args=["user", "ynmp_action"])
