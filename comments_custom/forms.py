import time
import datetime

from django import forms
from django.contrib.comments.forms import CommentForm
from comments_custom.models import CommentSimple
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
import settings

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH',3000)

class CommentFormSimple(CommentForm):
    comment = forms.CharField(label=_('Comment'), max_length=COMMENT_MAX_LENGTH)
    
    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return CommentSimple

    def check_for_duplicate_comment(self, new):
        """
        Check that a submitted comment isn't a duplicate. This might be caused
        by someone posting a comment twice. If it is a dup, silently return the *previous* comment.
        """
        possible_duplicates = self.get_comment_model()._default_manager.filter(
            content_type = new.content_type,
            object_pk = new.object_pk,
        )
        for old in possible_duplicates:
            if old.submit_date.date() == new.submit_date.date() and old.comment == new.comment:
                return old
                
        return new

    def get_comment_create_data(self):
        """
        Returns the dict of data to be used to create a comment. Subclasses in
        custom comment apps that override get_comment_model can override this
        method to add extra fields onto a custom comment model.
        """
        return dict(
            content_type = ContentType.objects.get_for_model(self.target_object),
            object_pk    = force_unicode(self.target_object._get_pk_val()),
            comment      = self.cleaned_data["comment"],
            submit_date  = datetime.datetime.now(),
            site_id      = settings.SITE_ID,
            is_public    = True,
            is_removed   = False,
        )


# Hacky hack hack
CommentFormSimple.base_fields.pop('url')
CommentFormSimple.base_fields.pop('email')
CommentFormSimple.base_fields.pop('name')

