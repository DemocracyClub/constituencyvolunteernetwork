from rules import AssignToAll, AssignToConstituency

gather_candidate_cambridge = AssignToConstituency("bar-cambridge", "cambridge", "http://www.theyworkforyou.com/gather/cambridge/%s")
gather_candidate_info = AssignToAll("gather-candidate-information", "http://www.theyworkforyou.com/gather/%s")
