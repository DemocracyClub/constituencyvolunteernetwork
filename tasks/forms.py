import re

from django import forms

import settings
from utils import TemplatedForm

from signup.models import Constituency
from tasks.models import Task

class AssignForm(TemplatedForm):
    tasks = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=Task.objects.all(), label="Choose one or more tasks")

class AssignConstituency(TemplatedForm):
    tasks = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=Task.objects.all(), label="Choose one or more tasks")
    constituencies = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=Constituency.objects.filter(year=settings.CONSTITUENCY_YEAR).order_by('name'), label="Choose one or more constituencies")
