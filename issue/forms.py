from django import forms

from models import Issue

class ConstituencyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class AddIssueForm(forms.Form):
    question = forms.CharField(required=True, max_length = 200)
    reference_url = forms.URLField(required=False)

    # Store user, so can be used to fill in default constituency
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(forms.Form, self).__init__(*args, **kwargs)

    def save(self, domain_override="", constituency=None):
        question = self.cleaned_data['question']
        reference_url = self.cleaned_data['reference_url']
        created_by = self.user

        issue = Issue.objects.create(question=question,
                                     reference_url=reference_url, 
                                     constituency=constituency,
                                     created_by=created_by)
        return issue

class ModerateIssueForm(forms.ModelForm):
    class Meta:
        model = Issue

    question = forms.CharField(required=True, max_length = 200)
    reference_url = forms.URLField(required=False)

    #def save(self, domain_override="", constituency=None):
    #    question = self.cleaned_data['question']
    #    reference_url = self.cleaned_data['reference_url']
    #    created_by = self.user
#
#        #issue = Issue.objects.create(question=question,
#        #                             reference_url=reference_url, 
#        #                             constituency=constituency,
#        #                             created_by=created_by)
#        #return issue
#        return None
#

        
        
