"""
    Signals for the task application.
    Sent when the state of a user on a task changes.
"""
import django.dispatch

task_assigned = django.dispatch.Signal(providing_args=["task_user"])
task_started = django.dispatch.Signal(providing_args=["task_user"])
task_ignored = django.dispatch.Signal(providing_args=["task_user"])
task_completed = django.dispatch.Signal(providing_args=["task_user"])
