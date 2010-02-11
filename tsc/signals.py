"""
    Signals for the The Straight Choice application.
    Sent when a user does an action with TSC
"""
import django.dispatch

leaflet_added = django.dispatch.Signal(providing_args=["user", "constituency"])
