from django import forms
import signals

import twfy
from utils import POSTCODE_RE
from utils import TemplatedForm
from models import CustomUser, Constituency, RegistrationProfile
from settings import CONSTITUENCY_YEAR

class UserForm(TemplatedForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    postcode = forms.CharField(label="Your postcode",
                               required=True)
    can_cc = forms.BooleanField(label="Let fellow constituents see my name and email",
                                help_text=("Important Note: this option "
                                           "means your information is "
                                           "essentially public (although "
                                           "not your postcode) so don't "
                                           "tick if you're very concerned "
                                           "about keeping your name and "
                                           "email private."),
                                required=False)

    def clean_email(self):
        """
        Validate that the email is not already in use.
        
        """
        user = CustomUser.objects.all()\
               .filter(email=self.cleaned_data['email'].lower())
        if user:
            raise forms.ValidationError('This email is already registered')
        return self.cleaned_data['email'].lower()

    def clean_postcode(self):
        code = self.cleaned_data['postcode']
        if not POSTCODE_RE.match(code):
            raise forms.ValidationError("Please enter a valid postcode")
        constituency_name = twfy.getConstituency(code)
        if constituency_name:
            constituency = Constituency.objects.all()\
                           .filter(name=constituency_name)\
                           .filter(year=CONSTITUENCY_YEAR)
            if constituency:
                self.cleaned_data['constituency'] = constituency[0]
            else:
                raise forms.ValidationError("Internal error: Constituency '%s' not found in DemocracyClub database" % constituency_name)
        else:
            raise forms.ValidationError("Unknown postcode")
        return code

        
    def save(self, domain_override=""):
        """
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User`` (by calling
        ``RegistrationProfile.objects.create_inactive_user()``).
        
        """
        email = self.cleaned_data['email']
        postcode = self.cleaned_data['postcode']
        can_cc = self.cleaned_data['can_cc']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        constituency = self.cleaned_data['constituency']
        user = CustomUser.objects.create(username=email,
                                         email=email,
                                         postcode=postcode,
                                         can_cc=can_cc,
                                         first_name=first_name,
                                         last_name=last_name,
                                         is_active=False)
        user.constituencies.add(constituency)
        user.save()
        profile = RegistrationProfile.objects.create_profile(user)
        signals.user_join.send(self, user=user)
        return profile
