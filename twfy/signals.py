import django.dispatch

pester_action_done = django.dispatch.Signal(providing_args=["user"])

