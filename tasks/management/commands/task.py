import os
from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from signup.models import CustomUser
from signup.models import Constituency
from signup.signals import user_touch
from tasks.models import TaskUser
from tasks.models import Task
import settings
from signup import twfy

class ConstituencyUserChain(object):
    def __init__(self, *constituencies):
        self.constituencies = self._flatten(*constituencies)
        self.current_idx = 0
        self.current_user_idx = 0
        self._set_current()
        
    def _set_current(self):
        self.current = self.constituencies[self.current_idx]\
                       .customuser_set.filter(is_active=True).all()
        
    def _flatten(self, *items):
        flattened = []
        for item in items:
            if isinstance(item, type([])):
                flattened.extend(item)
            else:
                flattened.append(item)
        return flattened

    def __iter__(self):
        return self
    
    def next(self):
        try:
            user = self.current[self.current_user_idx]
            self.current_user_idx += 1
            return user
        except IndexError:
            try:
                self.current_idx += 1
                self._set_current()
                self.current_user_idx = 0
                return self.next()
            except IndexError:
                raise StopIteration

class Command(BaseCommand):
    option_list =  BaseCommand.option_list + (
        make_option('--dry-run', '-n', dest='dry_run',
                    action="store_true",
                    help="Only show what would be done"),
        make_option('--slug', '-s', dest='task_slug',
                    action="store",
                    help="Only assign named task"),
        make_option('--max-number', '-m', dest='max_number',
                    action="store",
                    help="Maximum number of constituencies to consider"),
        make_option('--max-distance', '-d', dest='max_distance',
                    action="store",
                    help="Maximum distance of constituencies to consider"),
        make_option('--centre-postcode', '-p', dest='near_postcode',
                    action="store",
                    help="Assign constituency-wise in order of distance from postcode"),
        make_option('--emailfilter', '-e', dest='emailfilter',
                    action="store",
                    help="Only assign to users with emails containing")
        )
    help = "Assign tasks to users"
                        
    def handle(self, *args, **options):
        """
            The 'touch' command fires the user_touch signal on every
            user on the site. This allows tasks to :
            assign themselves
            to pre-existing users (in addition to new users, as handled
            by user_signup)
            """
        if not args:
            raise CommandError("Please specify a command, e.g. 'touch' or 'email'")
        if args[0] not in ('touch','email'):
            raise CommandError("Unknown command '%s'" % args[0])
        near_postcode = options.get('near_postcode', None)
        if not near_postcode:
            has_distance = options['max_distance']
            has_number = options['max_number']
            
            if has_distance and not has_number:
                raise CommandError("'max-distance' option requires a "
                                   "postcode")
            if has_number and not has_distance:
                raise CommandError("'max-number' option requires a "
                                   "postcode")
            
        if hasattr(options, 'max_distance') and not near_postcode:
            raise CommandError("'max-distance' option requires a postcode")
        max_distance = int(options['max_distance'] or 500)
        max_number = int(options['max_number'] or 100)
        if near_postcode:
            constituencies = []
            constituency_name = twfy.getConstituency(near_postcode)
            constituency = Constituency.objects.all()\
                           .filter(name=constituency_name)\
                           .get(year=settings.CONSTITUENCY_YEAR)
            neighbours = constituency.neighbors(limit=max_number,
                                                within_km=max_distance)
            users = ConstituencyUserChain(constituency, neighbours)

        else:
            users = CustomUser.objects.all()
        emailfilter = options.get('emailfilter', '')
        if emailfilter:
            users = users.filter(email__icontains=emailfilter)
        task_slug = options.get('task_slug', None)
        dry_run = options.get('dry_run', False)
        for user in users:
            msg = "user %s" % user
            if args[0] == "touch":
                msg += "\n  touching:"
                responses = []
                if task_slug:
                    if dry_run:
                        print task_slug
                    else:
                        responses = user_touch.send(self,
                                                    user=user,
                                                    task_slug=task_slug)
                else:
                    for task in Task.objects.all():
                        if dry_run:
                            print  task.slug
                        else:
                            result = user_touch.send(self,
                                                     user=user,
                                                     task_slug=task.slug)
                            responses.extend(result)
                    msg += "\n  ".join([x[1] for x in responses\
                                        if x[1]])
            elif args[0] == "email":
                emailed_on_this_round = []
                for task in TaskUser.objects.filter(emails_sent=0,
                                                    user=user):
                    if user.email not in emailed_on_this_round:
                        msg += "\n  emailing about %s" % task.task.slug
                        if not dry_run:
                            task.send_email()
                        emailed_on_this_round.append(user.email)
                    else:
                        msg += "\n   already emailed today"
                    
            print msg

