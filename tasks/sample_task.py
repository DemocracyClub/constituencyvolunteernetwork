import django.dispatch
from rules import TaskRouterAssignAll

class GatherCandidateInfo(TaskRouterAssignAll):
    task_slug = "gather-candidate-information"
    
    def url(self, user):
        return "http://www.theyworkforyou.com/gather/%s" % user.id

gather_candidate_info = GatherCandidateInfo()
