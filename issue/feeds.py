from django.contrib.syndication.feeds import Feed
from issue.models import Issue

class AllIssues(Feed):
    title = "Latest issues reported to Democracy Club"
    link = "/"
    description = title

    def items(self):
        return Issue.objects.order_by('-created_at','-id')

    def item_link(self, item):
        return item.constituency.get_absolute_url()
