from rules import assign_to_all, assign_to_constituency

# You have to assign the return value somewhere or the function wont be kept around for the signal
gather_candidate_information = assign_to_all("gather-candidate-information", "http://www.theyworkforyou.com/gather/%s")

gather_candidate_cambridge = assign_to_constituency("bar-cambridge", "http://www.theyworkforyou.com/gather/cambridge/%s", "cambridge")

class Rule:
    def __init__(self):
        self.register()

    def register(self):
        pass

class AssignToAll(Rule):
    def __init__(self, task_slug, url):
        

    def register(self):
        user_join.connect(self.callback_assign)
        user_touch.connect(self.callback_assign)
    
    def callback_assign(sender, **kwargs):
        print "Signal received %s" % kwargs['user']
        user = kwargs['user']
        task = Task.objects.get(slug=self.task_slug)
        
        try: # Make sure we're not already assigned this task, unless we want to
             # somehow assign a task multiple times for different constituencies?
            TaskUser.objects.get(user=user, task=task)
        except TaskUser.DoesNotExist:
            TaskUser.objects.assign_task(task, user, self.url(user, task))
            
    def url(self, user, task):
        return self.url % user
    
class GatherCandidateInformation(rules.AssignToAll):
    task_slug = "gather-candidate-information"
    url = "http://www.theyworkforyou.com/gather/%s"
    
gather_candidate_info = GatherCanddiateInformation()
