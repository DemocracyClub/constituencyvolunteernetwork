import re

from django import forms

from signup.models import Constituency
from tasks.models import Task

from utils import TemplatedForm

class AssignForm(TemplatedForm):
    tasks = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=Task.objects.all(), label="Choose one or more tasks")
