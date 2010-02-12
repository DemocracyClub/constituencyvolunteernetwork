"""
    Signals for the Issue application.
    Sent when a user does an action with regard to local issues.
"""
import django.dispatch

issue_added = django.dispatch.Signal(providing_args=["user"])
issue_moderated = django.dispatch.Signal(providing_args=["user"])

