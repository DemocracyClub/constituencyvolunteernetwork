from django import template
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponseRedirect
from django.contrib import comments
from django.contrib.comments import signals

@permission_required("comments.can_moderate")
def delete(request, comment_id, next=None):
    """
    Context:
        comment
            the flagged `comments.comment` object
    """
    comment = get_object_or_404(comments.get_model(), pk=comment_id, site__pk=settings.SITE_ID)

    # Delete on GET
    comment.delete()

    return HttpResponseRedirect(next)
