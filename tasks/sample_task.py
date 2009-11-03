from signup.signals import user_join, user_login, user_touch
from models import Task, TaskUser

from rules import assign_to_all

gather_candidate_information = assign_to_all("gather-candidate-information", "http://www.theyworkforyou.com/gather/%s")
# assign_to_constituency("gather-candidate-information", "http://www.theyworkforyou.com/gather/cambridge/%s", "cambridge")