"""
    Signals for the task application.
    Sent when the state of a user on a task changes.
"""
import django.dispatch

task_assigned = django.dispatch.Signal(providing_args=["user", "task"])
task_started = django.dispatch.Signal(providing_args=["user", "task"])
task_ignored = django.dispatch.Signal(providing_args=["user", "task"])
task_completed = django.dispatch.Signal(providing_args=["user", "task"])
