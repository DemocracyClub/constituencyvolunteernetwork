import re

from django import forms

from signup.models import CustomUser
from utils import TemplatedForm
from models import Invitation

import signals

import strings

def _extractEmails(emails_string):
    if "," in emails_string:
        delimiter = ","
    elif "\n" in emails_string:
        delimiter = "\n"
    elif " " in emails_string:
        delimiter = " "
    else:
        delimiter = "NONE"
    emails = emails_string.lower().split(delimiter)
    emails = [x.strip() for x in emails if x.strip()]
    good_emails = []
    bad_emails = []
    for addr in emails:
            match = re.match(r".*?([a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}).*", addr)
            if match:
                addr = match.group(1)                
                good_emails.append(addr)
            else:
                bad_emails.append(addr)
    if bad_emails:
        if len(bad_emails) == 1:
            msg = "%s is not a valid email address" % bad_emails[0]
        else:
            msg = ", ".join(bad_emails[:-1]) \
                  + " and %s are not valid email addresses" % bad_emails[-1]
        raise forms.ValidationError(msg)
    return good_emails
    
class InviteForm(TemplatedForm):
    honeypot = forms.CharField(required=False,)
    email = forms.CharField(label="Email addresses",
                            widget=forms.Textarea(attrs={'rows':10,
                                                         'cols':40}),
                            required=True)
    message = forms.CharField(label="A short message",
                              max_length=500,
                              widget=forms.Textarea(attrs={'rows':8,
                                                           'cols':40}),
                              required=False,
                              initial=strings.INVITE_TEXT)
    
    def clean_email(self):
        """
        Validate that the email is not already used by a registered 
        user and has not already been sent an invite.
        """
        addresses = _extractEmails(self.cleaned_data['email'])
        to_invite = []
        for email in addresses:
            user = CustomUser.objects.all()\
                   .filter(email=email)
            if user:
                continue
            invite = Invitation.objects.all()\
                    .filter(email=email.lower())
            if invite:
                continue
            to_invite.append(email)
            
        return to_invite
        
    def clean_honeypot(self): # Honeypot to catch bots. Will this work?
        if self.cleaned_data['honeypot'] != "":
            raise forms.ValidationError(strings.INVITE_ERROR_HONEYPOT)
        else:
            return self.cleaned_data['honeypot']
        
    def save(self, user):
        for email in self.cleaned_data['email']:
            message = self.cleaned_data['message']
            Invitation.objects.create_invitation(email=email,
                                                 message=message,
                                                 user=user)

        signals.invitation_sent.send(self, user=user)

