from django import forms

from utils import TemplatedForm
from models import Issue

class ConstituencyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class AddIssueForm(TemplatedForm):
    question = forms.CharField(required=True, max_length = 200)
    reference_url = forms.URLField(required=False)

    # Set up default values for constituency drop down, or if the user has
    # only one constituency, make it a hidden field.
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TemplatedForm, self).__init__(*args, **kwargs)

    def save(self, domain_override="", constituency=None):
        question = self.cleaned_data['question']
        reference_url = self.cleaned_data['reference_url']
        created_by = self.user

        issue = Issue.objects.create(question=question,
                                     reference_url=reference_url, 
                                     constituency=constituency,
                                     created_by=created_by)
        return issue


        
