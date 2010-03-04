import datetime

from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.comments.models import BaseCommentAbstractModel, Comment
from django.contrib.comments.managers import CommentManager
from django.contrib.comments.signals import comment_was_posted
from django.contrib.sites.models import Site
from django.conf import settings
from signup.models import Model, CustomUser, Constituency
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH',3000)

class NotifyComment(Model):
    """
        Specifies that a user should be notified when a comment is posted on
        a constituency discussion page
    """
    
    class Types:
        none = 0 # No notify
        every = 1 # Notify for every comment
        digest = 2 # Email a weekly digest
    
        strings = (
            (none, 'Don\'t notify'),
            (every, 'Notify for every comment'),
            (digest, 'Email a weekly digest'),
        )

    user = models.ForeignKey(CustomUser)
    constituency = models.ForeignKey(Constituency)
    created_at = models.DateTimeField(auto_now_add=True)
    notify_type = models.SmallIntegerField(choices=Types.strings)

    def on(self):
        self.notify_type = self.Types.every

    def off(self):
        self.notify_type = self.Types.none

    def send_email(self, comment, first):
        slug = comment.content_object.slug
        login_key = self.user.registrationprofile_set.get().activation_key
        constituency_link = reverse("constituency", kwargs={'slug': slug,
                                                            'login_key': login_key, })

        context = {'comment': comment,
                   'constituency': comment.content_object,
                   'user': self.user,
                   'first': first,
                   'link': constituency_link,
                   'site': Site.objects.get_current(),}

        subject = "Comment posted in %s on Democracy Club" % (comment.content_object.name)
        message_plain = render_to_string("comments/email_comments.txt",
                                         context)
        msg = EmailMultiAlternatives(subject,
                                     message_plain,
                                     settings.DEFAULT_FROM_EMAIL,
                                     [self.user.email, ])
        msg.send()

MODERATION_REASON = (
    ('none', ''),
    ('spam', 'Comment is spam'),
    ('partisan', 'Comment advocates particular party or candidate'),
    ('interest', 'Comment advocates or advertises a particular interest group'),
    ('abusive', 'Comment is abusive'),
)

class CommentSimple(BaseCommentAbstractModel):
    moderation_reasons = dict(MODERATION_REASON)
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
    removal_reason = models.CharField(max_length=20,
                                      choices=MODERATION_REASON,
                                      default='none')

    @property
    def long_removal_reason(self):
        return self.moderation_reasons[self.removal_reason]

    # Manager
    objects = CommentManager()

    class Meta:
        db_table = "custom_comments"
        ordering = ('submit_date',)
        permissions = [("can_moderate", "Can moderate comments")]
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __unicode__(self):
        return "%s: %s..." % (self.user,
                              self.comment[:50])

    def save(self, force_insert=False, force_update=False):
        if self.submit_date is None:
            self.submit_date = datetime.datetime.now()
        super(CommentSimple, self).save(force_insert, force_update)

def callback_comment_posted(**kwargs):
    sender = kwargs['sender']
    comment = kwargs['comment'] 
    request = kwargs['request'] 
    constituency = comment.content_object

    users = constituency.customuser_set.all()
    
    for user in users:
        if user != comment.user:
            try:
                notify_obj = NotifyComment.objects.get(user=user,
                                                       constituency=constituency)
            except NotifyComment.DoesNotExist:
                notify_obj = None

            if notify_obj:
                if notify_obj.notify_type == NotifyComment.Types.every:
                    notify_obj.send_email(comment, False)
            else:
                # Send the email and notifications will be deactivated in the future
                notify_obj =  NotifyComment.objects.create(user=user,
                                                           constituency=constituency,
                                                           notify_type=NotifyComment.Types.none)
                notify_obj.send_email(comment, True)
    
comment_was_posted.connect(callback_comment_posted)
