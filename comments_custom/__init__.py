from django.core import urlresolvers

from comments_custom.models import CommentSimple
from comments_custom.forms import CommentFormSimple

def get_form():
    return CommentFormSimple

def get_model():
    return CommentSimple

def get_delete_url(comment):
    return urlresolvers.reverse("custom_comment_delete", args=(comment.id,)) 
