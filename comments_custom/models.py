from django.db import models
from django.contrib.comments.models import BaseCommentAbstractModel, Comment
from django.contrib.comments.managers import CommentManager
from django.conf import settings
from signup.models import CustomUser
from django.utils.translation import ugettext_lazy as _

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH',3000)

class CommentSimple(BaseCommentAbstractModel):
    """
        There must be a better way to subclass from Comment remove the fields
        instead of duplicating it...
    """

    user = models.ForeignKey(CustomUser, verbose_name=_('user'),
                    blank=True, null=True, related_name="%(class)s_comments")

    comment = models.TextField(_('comment'), max_length=COMMENT_MAX_LENGTH)

    # Metadata about the comment
    submit_date = models.DateTimeField(_('date/time submitted'), default=None)
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)
    is_public   = models.BooleanField(_('is public'), default=True,
                    help_text=_('Uncheck this box to make the comment effectively ' \
                                'disappear from the site.'))
    is_removed  = models.BooleanField(_('is removed'), default=False,
                    help_text=_('Check this box if the comment is inappropriate. ' \
                                'A "This comment has been removed" message will ' \
                                'be displayed instead.'))

    # Manager
    objects = CommentManager()

    class Meta:
        db_table = "custom_comments"
        ordering = ('submit_date',)
        permissions = [("can_moderate", "Can moderate comments")]
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __unicode__(self):
        return "%s: %s..." % (self.name, self.comment[:50])

    def save(self, force_insert=False, force_update=False):
        if self.submit_date is None:
            self.submit_date = datetime.datetime.now()
        super(CommentSimple, self).save(force_insert, force_update)
